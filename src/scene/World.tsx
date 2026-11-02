import React, { useMemo } from "react";
import * as THREE from "three";
import { useCurrentFrame } from "remotion";
import { useThree } from "@react-three/fiber";
import { TOTAL, FPS, LINE_F, SHOTS, towerState, shotAt, smooth, clamp01, FLOOR_BEATS, A, HAMMER_FREEZE, HAMMER_DROP, squeeze, footSink, CUT, BEACH, SPONGE } from "../story";

const mat=(color:string, roughness=0.9)=>new THREE.MeshStandardMaterial({color,roughness});
const stone=mat("#eee9dc"), stoneShade=mat("#c8c2b5"), grass=mat("#75a95d"), wood=mat("#9b6035"), darkWood=mat("#583b2d"), clay=mat("#a86e4c"), sand=mat("#d7bd8c"), darkSand=mat("#9b8064"), iron=mat("#45464a"), red=mat("#b7443c"), blue=mat("#477bb5"), gold=mat("#d6a84e");
const ease=(a:number,b:number,x:number)=>smooth(clamp01((x-a)/(b-a)));
function Stickman({x=0,z=0,scale=1,shirt="#397d69",pants="#34465f",hat="",tool="",rotation=0}:{x?:number;z?:number;scale?:number;shirt?:string;pants?:string;hat?:string;tool?:string;rotation?:number}){
 const tex=useMemo(()=>{const c=document.createElement('canvas');c.width=600;c.height=1000;const g=c.getContext('2d')!;g.lineCap='round';g.lineJoin='round';const ink='#241726';
  // bean head
  g.fillStyle='#fffdf7';g.strokeStyle=ink;g.lineWidth=17;g.beginPath();g.moveTo(300,65);g.bezierCurveTo(465,48,520,190,490,330);g.bezierCurveTo(470,445,390,485,300,480);g.bezierCurveTo(190,490,115,430,105,320);g.bezierCurveTo(88,185,145,65,300,65);g.fill();g.stroke();
  // face
  g.fillStyle=ink;g.beginPath();g.ellipse(245,260,13,19,0,0,Math.PI*2);g.ellipse(355,260,13,19,0,0,Math.PI*2);g.fill();g.lineWidth=10;g.beginPath();g.moveTo(260,345);g.quadraticCurveTo(300,365,340,345);g.stroke();
  // body
  g.fillStyle=shirt;g.strokeStyle=ink;g.lineWidth=16;g.beginPath();g.moveTo(220,490);g.quadraticCurveTo(300,460,380,490);g.lineTo(405,730);g.quadraticCurveTo(300,770,195,730);g.closePath();g.fill();g.stroke();
  // arms
  g.strokeStyle=ink;g.lineWidth=19;g.beginPath();g.moveTo(220,530);g.lineTo(130,650);g.lineTo(100,740);g.moveTo(380,530);g.lineTo(470,640);g.lineTo(500,730);g.stroke();
  // legs
  g.lineWidth=22;g.beginPath();g.moveTo(245,735);g.lineTo(220,900);g.moveTo(355,735);g.lineTo(390,900);g.stroke();g.lineWidth=24;g.beginPath();g.moveTo(220,900);g.lineTo(180,920);g.moveTo(390,900);g.lineTo(430,920);g.stroke();
  if(hat){g.fillStyle=hat;g.strokeStyle=ink;g.lineWidth=14;g.beginPath();g.rect(190,55,220,25);g.fill();g.stroke();g.beginPath();g.rect(235,5,130,60);g.fill();g.stroke();}
  if(tool){g.strokeStyle=ink;g.lineWidth=18;g.beginPath();g.moveTo(505,730);g.lineTo(540,500);g.stroke();g.fillStyle=gold;g.fillRect(500,480,85,24);}
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;},[shirt,pants,hat,tool]);
 return <sprite position={[x,1.9*scale,z]} scale={[1.45*scale,2.45*scale,1]} rotation={[0,rotation,0]}><spriteMaterial map={tex} transparent depthWrite={false}/></sprite>;
}
function Tower({floors=8,tilt=.1, moss=0,curve=0}:{floors?:number;tilt?:number;moss?:number;curve?:number}){
 const items=[];for(let i=0;i<8;i++){const visible=i<floors;const height=5.4;const lift= i*height;const bend=curve*Math.max(0,i-2)*.012;
  items.push(<group key={i} position={[Math.sin(tilt)*lift + bend*lift, lift*Math.cos(tilt),0]} rotation={[0,0,-tilt + bend]} visible={visible}>
   <mesh position={[0,2.7,0]}><cylinderGeometry args={[7.2,7.2,5.25,48]}/><meshStandardMaterial color="#eee9dc" roughness={0.9}/></mesh>
   <mesh position={[0,5.35,0]}><cylinderGeometry args={[7.65,7.65,.35,48]}/><meshStandardMaterial color="#c8c2b5" roughness={0.9}/></mesh>
   <mesh position={[0,.22,0]}><cylinderGeometry args={[7.55,7.55,.35,48]}/><meshStandardMaterial color="#c8c2b5" roughness={0.9}/></mesh>
   {Array.from({length:14},(_,j)=>{const a=j/14*Math.PI*2;return <mesh key={j} position={[Math.cos(a)*6.8,4.35,Math.sin(a)*6.8]}><cylinderGeometry args={[.22,.22,1.7,8]}/><meshStandardMaterial color="#c8c2b5" roughness={0.9}/></mesh>})}
   {Array.from({length:14},(_,j)=>{const a=j/14*Math.PI*2;return <mesh key={'c'+j} position={[Math.cos(a)*6.8,1.1,Math.sin(a)*6.8]}><cylinderGeometry args={[.2,.2,1.9,8]}/><meshStandardMaterial color="#eee9dc" roughness={0.9}/></mesh>})}
   {moss>.1&&<mesh position={[0,5.5,7.22]}><boxGeometry args={[2.5,.25,.08]}/><meshStandardMaterial color="#4d7944" transparent opacity={moss*.7}/></mesh>}
  </group>);
 }
 return <group>{items}</group>;
}
function Piazza(){return <group><mesh rotation={[-Math.PI/2,0,0]} position={[0,-.15,0]}><planeGeometry args={[500,500]}/><meshStandardMaterial color="#75a95d" roughness={0.9}/></mesh><mesh position={[-26,8,-18]}><boxGeometry args={[38,16,15]}/><meshStandardMaterial color="#eee9dc" roughness={0.9}/></mesh><mesh position={[-26,16,-18]}><coneGeometry args={[22,9,4]}/><meshStandardMaterial color="#c8c2b5" roughness={0.9}/></mesh>{[-42,-34,-26,-18,-10].map((x,i)=><mesh key={i} position={[x,3,-18]}><cylinderGeometry args={[.35,.6,6,7]}/><meshStandardMaterial color="#426c42"/></mesh>)}</group>}
function Cutaway(){return <group position={[0,0,0]}><mesh position={[0,-7,0]}><boxGeometry args={[26,14,12]}/><meshStandardMaterial color="#a86e4c" roughness={0.9}/></mesh><mesh position={[0,-.4,0]}><boxGeometry args={[27,.8,13]}/><meshStandardMaterial color="#d7bd8c" roughness={0.9}/></mesh>{[-8,-4,0,4,8].map(x=><mesh key={x} position={[x,-3,6.1]}><boxGeometry args={[.16,7,.16]}/><meshStandardMaterial color="#45464a" roughness={0.9}/></mesh>)}</group>}
function Stage({id,frame}:{id:number;frame:number}){
 if(id===10){const s=squeeze(frame);return <group><mesh rotation={[-Math.PI/2,0,0]} position={[0,-.3,0]}><planeGeometry args={[100,100]}/><meshStandardMaterial color="#9b6035" roughness={0.9}/></mesh><mesh position={[0,1.2,0]} scale={[2.8,1.2*(1-s*.35),1.4]}><boxGeometry/><meshStandardMaterial color="#e7d33c" roughness={.4}/></mesh>{Array.from({length:5},(_,i)=><mesh key={i} position={[(i-2)*.65,.3,-1]}><sphereGeometry args={[.09,12,8]}/><meshStandardMaterial color="#6fb9d5"/></mesh>)}</group>}
 if(id===11){const sink=footSink(frame);return <group><mesh rotation={[-Math.PI/2,0,0]}><planeGeometry args={[100,100]}/><meshStandardMaterial color="#d7bd8c" roughness={0.9}/></mesh><mesh rotation={[-Math.PI/2,0,0]} position={[0,-.05,-12]}><planeGeometry args={[100,22]}/><meshStandardMaterial color="#5799c1"/></mesh><mesh position={[0,1.1-sink*.7,0]}><boxGeometry args={[.85,2.1,1.0]}/><meshStandardMaterial color="#d6a078"/></mesh></group>}
 if(id===4||id===12||id===16)return <Cutaway/>;
 return <Piazza/>;
}
export const World:React.FC=()=>{const f=useCurrentFrame();const {camera,scene}=useThree();const shot=shotAt(f);const id=shot.id;const local=f-shot.a;const st=towerState(id,f);const isCut=[4,12,16].includes(id);const isModern=[1,15,16,17].includes(id);const floors=id===3?Math.min(3,Math.max(0,(f-LINE_F[2])/32)):st.floors;
 const positions:Record<number,[number,number,number,number]>={1:[-8,13,43,0],2:[12,9,34,0],3:[4,15,35,0],4:[0,4,28,0],5:[13,7,19,0],6:[-9,9,21,0],7:[-18,10,36,0],8:[22,12,38,0],9:[22,12,38,0],10:[0,5,14,0],11:[4,3,12,0],12:[-12,1,24,0],13:[30,23,50,0],14:[12,15,34,0],15:[13,7,19,0],16:[-12,3,23,0],17:[-8,13,43,0]};
 const p=positions[id]||[0,10,35,0];const target:THREE.Vector3=new THREE.Vector3(isCut?0:0,isCut?-2:12,0);const push=1+Math.min(local,90)*.0018;camera.position.set(p[0]/push,p[1]/push,p[2]/push);camera.lookAt(target);(camera as THREE.PerspectiveCamera).fov= id===5||id===15?34:42;(camera as THREE.PerspectiveCamera).updateProjectionMatrix();
 scene.background=new THREE.Color(id===7||id===8||id===9||id===13?'#f3b77c':'#82b5e8');
 const showPiazza=[1,2,3,5,6,7,8,9,13,14,15,17].includes(id);
 return <>
  <ambientLight intensity={1.25}/><directionalLight position={[-25,40,25]} intensity={2.2} castShadow/><hemisphereLight args={['#c8e2ff','#8e795e',.65]}/>
  {showPiazza&&<Piazza/>}{!showPiazza&&<Stage id={id} frame={f}/>}
  {showPiazza&&<Tower floors={id===2?0:id===3?floors:st.floors} tilt={st.tilt} moss={st.moss} curve={st.curve}/>}
  {id===1||id===17?<><Stickman x={-5} z={11} shirt="#e9a33a" pants="#354f85"/><Stickman x={1} z={13} shirt="#4d9d80" pants="#3f465c" hat="#2c2a30"/></>:null}
  {id===2||id===3||id===5||id===6||id===14?<><Stickman x={5} z={9} shirt="#397d69" pants="#654b3b" hat="#e5d8b8" tool="hammer"/><Stickman x={9} z={11} shirt="#a94e4b" pants="#4a5365" hat="#b8a1a0"/><Stickman x={-7} z={8} shirt="#4f7fa8" pants="#5a493e" hat="#d4c7a2"/></>:null}
  {id===7||id===9?<>{Array.from({length:8},(_,i)=><Stickman key={i} x={-13+i*3.2} z={10+(i%2)*1.2} shirt={i%2?'#a34d43':'#507a55'} pants="#45475b" hat="#d8d0c0" rotation={.1}/>)}</>:null}
  {id===14?<Stickman x={-2} z={12} shirt="#9d4c40" pants="#4b4c55" hat="#b64a3f"/>:null}
  {id===15||id===16?<><Stickman x={8} z={10} shirt="#e77f36" pants="#4d5361" hat="#f4f2df"/><Stickman x={12} z={12} shirt="#e77f36" pants="#4d5361" hat="#f4f2df"/></>:null}
  {id===17?<Stickman x={-1} z={5} scale={.7} shirt="#e17c2c" pants="#454f65" hat="#f2e9d6"/>:null}
  {id===6&&<mesh position={[-4,7,7]} rotation={[0,0,local>HAMMER_FREEZE?-.7:0]}><boxGeometry args={[.2,3,.2]}/><meshStandardMaterial color="#9b6035" roughness={0.9}/></mesh>}
  {id===13&&<mesh position={[0,2,0]}><boxGeometry args={[3,.3,3]}/><meshStandardMaterial color="#c8c2b5" roughness={0.9}/></mesh>}
  {id===16&&<mesh position={[-5,-2,5]}><cylinderGeometry args={[.35,.35,5,12]}/><meshStandardMaterial color="#45464a" roughness={0.9}/></mesh>}
 </>;
};
