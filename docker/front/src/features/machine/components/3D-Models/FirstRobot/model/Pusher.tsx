import { useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

export const Pusher = () => {
  const gltf = useLoader(GLTFLoader, '/gltf/Robot_1_Pusher.gltf');
  return <primitive object={gltf.scene} />;
};
