import React, { useRef } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useLoader } from "@react-three/drei";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { TextureLoader } from "three";

const ModelViewer = ({ modelPath, texturePath }) => {
  const obj = useLoader(OBJLoader, modelPath);
  const texture = useLoader(TextureLoader, texturePath);

  return (
    <Canvas camera={{ position: [0, 1, 3], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh>
        <primitive object={obj} />
        {texture && <meshStandardMaterial map={texture} />}
      </mesh>
      <OrbitControls />
    </Canvas>
  );
};

export default ModelViewer;
