import { Matrix4x4 } from "./structs/Matrix4x4";
import { Mesh } from "./structs/Mesh";
import { ProjMatrix } from "./structs/ProjMatrix";
import { Vec3d } from "./structs/Vectors";
import type { Tris } from "./structs/Tris";
import { generateLg } from "./structs/Texture";


const texture = generateLg()
let drawEdges = false

export type Ctx = CanvasRenderingContext2D

export class CameraEngine {
    public readonly cameraInfo: CameraInfo
    public readonly cameraPos = new CameraPos();

    private lightPosNormalised: Vec3d = Vec3d.from(-4, -3, -7).normalise()
    private ctx: CanvasRenderingContext2D
    private eps = 0.001

    constructor(width: number, height: number) {
        this.cameraInfo = new CameraInfo(width, height)
    }

    public clear(ctx: Ctx) {
        ctx.fillStyle = 'rgb(31, 28, 28)'
        ctx.fillRect(0, 0, this.cameraInfo.width, this.cameraInfo.height);
    }

    public drawMesh(mesh: Mesh, ctx: Ctx) {
        this.ctx = ctx
        let cameraPos = this.cameraPos.cameraPos
        let meshToRender = new Mesh([])

        // eliminate opposite oriented tris
        for (let i = 0; i < mesh.triangles.length; i++) {
            let tris = mesh.triangles[i]
            let t = tris.p1.subtract(cameraPos)
            let dotProduct = t.dotProduct(tris.normal)
            if (dotProduct < 0) {
                meshToRender.add(tris)
            }
        }

        // project
        for (let i = 0; i < meshToRender.triangles.length; i++) {
            meshToRender.triangles[i] = this.project(meshToRender.triangles[i])
            meshToRender.triangles[i].setArea()
            meshToRender.triangles[i].setMaxY()
            meshToRender.triangles[i].setMinY()
            meshToRender.triangles[i].calcLinesCoeffs()
        }

        // meshToRender.triangles
        //     .sort((t1, t2) => t2.maxY - t1.maxY)

        let data = this.ctx.getImageData(0, 0, this.cameraInfo.width, this.cameraInfo.height)
        for (let y = 0; y < this.cameraInfo.height; y++) {
            let y3d = this.yTo3dSpace(y)

            let trisAtHeight = meshToRender.triangles.filter(tris => {
                return tris.maxY >= y3d && tris.minY <= y3d
            })
            if (trisAtHeight.length === 0) {
                continue
            }

            let xRanges = trisAtHeight.map(tris => tris.getXRange(y3d))
            let xSharedSet = new Set<number>()
            xRanges.forEach(range => {
                xSharedSet.add(range[0])
                xSharedSet.add(range[1])
            })
            let xShared = [...xSharedSet].sort((t1, t2) => t1 - t2)
            let x2dRange = xShared.map(x => [this.x3dTo2dSpace(x), -1])

            for (let i = 1; i < xShared.length; i++) {
                let x1 = xShared[i - 1]
                let x2 = xShared[i]
                let trisIndexesWithZ = []

                for (let j = 0; j < trisAtHeight.length; j++) {
                    let tris = trisAtHeight[j]

                    if (!(tris.pointInside(x1, y3d) && tris.pointInside(x2, y3d)) && !(tris.pointInside(x1 + this.eps, y3d) && tris.pointInside(x2 - this.eps, y3d)))
                        continue

                    trisIndexesWithZ.push([j, tris.calcZOn(x1, y3d), tris.calcZOn(x2, y3d)])
                }

                if (trisIndexesWithZ.length == 0)
                    continue

                x2dRange[i][1] = trisIndexesWithZ.sort((t1, t2) => {
                    if (t1[1] === t2[1])
                        return t1[2] - t2[2]
                    return t1[1] - t2[1]
                })[0][0]
            }

            for (let i = 1; i < x2dRange.length; i++) {
                let x1 = x2dRange[i - 1][0]
                let x2 = x2dRange[i][0]
                let trisIndex = x2dRange[i][1]

                if (trisIndex === -1 || (x1 < 0 && x2 < 0) || (x1 > this.cameraInfo.width - 1 && x2 > this.cameraInfo.width - 1))
                    continue

                if (x1 < 0)
                    x1 = 0

                if (x2 > this.cameraInfo.width - 1)
                    x2 = this.cameraInfo.width - 1

                let tris = trisAtHeight[trisIndex]

                // lightning
                let lightStrength = tris.normal.dotProduct(this.lightPosNormalised)
                lightStrength = Math.max(Math.min(lightStrength, 1), 0.15)

                for (let x = x1; x < x2; x++) {
                    let textureCoords = tris.getTextureCoords(this.xTo3dSpace(x), y3d)
                    let color = texture.getPx(textureCoords.x, textureCoords.y)
                    let dataStart = (y * data.width + x) * 4;
                    data.data[dataStart] = color.r * lightStrength
                    data.data[dataStart + 1] = color.g * lightStrength
                    data.data[dataStart + 2] = color.b * lightStrength
                    data.data[dataStart + 3] = 255
                }
            }
        }
        this.ctx.putImageData(data, 0, 0)

        if (drawEdges) {
            ctx.strokeStyle = 'rgba(0,0,200, 0.7)'
            ctx.lineWidth = 2
            for (const tris of meshToRender.triangles) {
                ctx.beginPath()
                let x = this.scaleXToCanvas(tris.vertexes[2].x)
                let y = this.scaleYToCanvas(tris.vertexes[2].y)
                ctx.lineTo(x, y)
                for (let j = 0; j < 3; j++) {
                    x = this.scaleXToCanvas(tris.vertexes[j].x)
                    y = this.scaleYToCanvas(tris.vertexes[j].y)
                    ctx.lineTo(x, y)
                }
                ctx.stroke()
            }
        }
    }

    private project(tris: Tris): Tris {
        const projMatrix = this.cameraInfo.projMatrix;
        const rotationMatrix = this.cameraPos.rotMatrix
        const vCamera = this.cameraPos.cameraPos
        const projTris = tris.copy()

        for (let i = 0; i < 3; i++) {
            let temp = tris.vertexes[i].subtract(vCamera)
            temp = rotationMatrix.multiplyWithVec3d(temp)
            projTris.vertexes[i] = projMatrix.projectVec(temp)
        }

        return projTris
    }

    private scaleXToCanvas(xCoord: number): number {
        return (xCoord + 1) * (this.cameraInfo.width / 2)
    }

    private scaleYToCanvas(yCoord: number): number {
        return (yCoord + 1) * (this.cameraInfo.height / 2)
    }

    private xTo3dSpace(xCoord: number): number {
        return (2 * xCoord) / this.cameraInfo.width - 1
    }

    private yTo3dSpace(yCoord: number): number {
        return (2 * yCoord) / this.cameraInfo.height - 1
    }

    private x3dTo2dSpace(x3d: number): number {
        return Math.ceil((x3d + 1) * this.cameraInfo.width / 2)
    }

    // private y3dTo2dSpace(y3d: number): number {
    //     return Math.ceil((y3d + 1) * this.cameraInfo.width / 2)
    // }

}

class CameraInfo {
    public fov = Math.PI / 8;
    private fovChange = Math.PI / 32;
    public zFar = 100000;
    public zNear = 0.1;
    public width: number;
    public height: number;
    public projMatrix: ProjMatrix;

    constructor(width: number, height: number) {
        this.width = width;
        this.height = height;
        this.projMatrix = this.createProjectionMatrix()
    }

    public createProjectionMatrix(): ProjMatrix {
        return new ProjMatrix(this.fov, this.zFar, this.zNear, this.width, this.height);
    }

    public posZoom() {
        this.fov -= this.fovChange
        this.projMatrix = this.createProjectionMatrix()
    }

    public negZoom() {
        this.fov += this.fovChange
        this.projMatrix = this.createProjectionMatrix()
    }

}

class CameraPos {
    private vCamera = Vec3d.from(0, 0, -6)
    private moveFactor = 0.1;
    private rotateFactor = Math.PI / 128;
    private rotationMatrix = Matrix4x4.identity()
    private rotationMatrixInverse = Matrix4x4.identity()
    private translationVecs = [
        Vec3d.from(this.moveFactor, 0, 0),
        Vec3d.from(-this.moveFactor, 0, 0),
        Vec3d.from(0, this.moveFactor, 0),
        Vec3d.from(0, -this.moveFactor, 0),
        Vec3d.from(0, 0, this.moveFactor),
        Vec3d.from(0, 0, -this.moveFactor)]
    private rotXPos = Matrix4x4.rotationX(this.rotateFactor)
    private rotXNeg = Matrix4x4.rotationX(-this.rotateFactor)
    private rotYPos = Matrix4x4.rotationY(-this.rotateFactor)
    private rotYNeg = Matrix4x4.rotationY(this.rotateFactor)
    private rotZPos = Matrix4x4.rotationZ(this.rotateFactor)
    private rotZNeg = Matrix4x4.rotationZ(-this.rotateFactor)

    public get rotMatrix(): Matrix4x4 {
        return this.rotationMatrix
    }

    public moveForward() {
        this.translate(4);
    }

    public moveBackward() {
        this.translate(5);
    }

    public moveLeft() {
        this.translate(1);
    }

    public moveRight() {
        this.translate(0);
    }

    public moveUp() {
        this.translate(3);
    }

    public moveDown() {
        this.translate(2);
    }

    private translate(i: number) {
        const translationVec = this.translationVecs[i]
        const rotatedVec = this.rotationMatrixInverse.multiplyWithVec3d(translationVec)
        this.vCamera = this.vCamera.add(rotatedVec)
    }

    public rotatePosX() {
        this.rotationMatrix = this.rotXPos.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public rotateNegX() {
        this.rotationMatrix = this.rotXNeg.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public rotatePosY() {
        this.rotationMatrix = this.rotYPos.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public rotateNegY() {
        this.rotationMatrix = this.rotYNeg.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public rotatePosZ() {
        this.rotationMatrix = this.rotZPos.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public rotateNegZ() {
        this.rotationMatrix = this.rotZNeg.multiply(this.rotationMatrix)
        this.rotationMatrixInverse = Matrix4x4.matrixInverse(this.rotationMatrix)
    }

    public get cameraPos(): Vec3d {
        return this.vCamera
    }

}