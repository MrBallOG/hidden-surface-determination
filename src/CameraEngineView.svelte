<script lang="ts">
	import { CameraEngine } from './CameraEngine';
	import { onMount } from 'svelte';
	import { defaultPlain, Mesh, texturedCube } from './structs/Mesh';

	const width = 1200;
	const height = 700;
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D;

	let camera = new CameraEngine(width, height);
	let scene: Mesh = new Mesh([]);
	let cube1 = texturedCube().translateZ(2).translateX(-1);
	let cube2 = texturedCube().translateZ(2).translateX(0.5);
	// let cube3 = texturedCube()
	//     .translateZ(2)
	//     .translateX(1.5)
	// let cube4 = texturedCube()
	//     .translateZ(4)
	//     .translateX(0.5)

	// let cube5 = texturedCube()
	//     .translateZ(4)
	//     .translateX(-1.5)

	// let cube6 = texturedCube()
	//     .translateZ(4)
	//     .translateX(2)

	// let cube7 = texturedCube()
	//     .translateZ(4)
	//     .translateX(-3)

	// let cube8= texturedCube()
	//     .translateZ(6)
	//     .translateX(2)

	// let cube9 = texturedCube()
	//     .translateZ(6)
	//     .translateX(-3)

	// let plain = defaultPlain()
	//     .translateX(-3)
	//     .translateZ(3)
	//     .translateY(1.1)

	scene.addMesh(cube1);
	scene.addMesh(cube2);
	// scene.addMesh(cube3);
	// scene.addMesh(cube4);
	// scene.addMesh(cube5);
	// scene.addMesh(cube6);
	// scene.addMesh(cube7);
	// scene.addMesh(cube8);
	// scene.addMesh(cube9);

	onMount(() => {
		canvas.width = width;
		canvas.height = height;
		ctx = canvas.getContext('2d');
		camera.clear(ctx);
		camera.drawMesh(scene, ctx);
	});

	const update = () => {
		camera.clear(ctx);
		camera.drawMesh(scene, ctx);
	};

	const moveActions: [string, () => void][] = [
		['Forward', () => camera.cameraPos.moveForward()],
		['Backward', () => camera.cameraPos.moveBackward()],
		['Up', () => camera.cameraPos.moveUp()],
		['Down', () => camera.cameraPos.moveDown()],
		['Left', () => camera.cameraPos.moveLeft()],
		['Right', () => camera.cameraPos.moveRight()]
	];

	const rotateActions: [string, () => void][] = [
		['Rotate X', () => camera.cameraPos.rotatePosX()],
		['Rotate -X', () => camera.cameraPos.rotateNegX()],
		['Rotate Y', () => camera.cameraPos.rotatePosY()],
		['Rotate -Y', () => camera.cameraPos.rotateNegY()],
		['Rotate Z', () => camera.cameraPos.rotatePosZ()],
		['Rotate -Z', () => camera.cameraPos.rotateNegZ()]
	];

	const handleKeydown = (event) => {
		let key = event.key;
		if (key == 'a') {
			moveActions[4][1]();
			update();
		} else if (key === 'd') {
			moveActions[5][1]();
			update();
		} else if (key === 'w') {
			moveActions[2][1]();
			update();
		} else if (key === 's') {
			moveActions[3][1]();
			update();
		} else if (key === 'q') {
			moveActions[1][1]();
			update();
		} else if (key === 'e') {
			moveActions[0][1]();
			update();
		} else if (key === 'j') {
			rotateActions[2][1]();
			update();
		} else if (key === 'l') {
			rotateActions[3][1]();
			update();
		} else if (key === 'i') {
			rotateActions[0][1]();
			update();
		} else if (key === 'k') {
			rotateActions[1][1]();
			update();
		} else if (key === 'u') {
			rotateActions[4][1]();
			update();
		} else if (key === 'o') {
			rotateActions[5][1]();
			update();
		} else if (key === 'z') {
			camera.cameraInfo.posZoom();
			update();
		} else if (key === 'x') {
			camera.cameraInfo.negZoom();
			update();
		} else if (key === 'r') {
			camera = new CameraEngine(width, height);
			update();
		}
	};
</script>

<svelte:window on:keydown={handleKeydown} />

<div>
	<canvas id="camera_canvas" bind:this={canvas} />
</div>

<style>
	div {
		display: flex;
		justify-content: center;
		height: 100%;
	}
	canvas {
		padding: 0;
		margin: auto;
		display: block;
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
	}
</style>
