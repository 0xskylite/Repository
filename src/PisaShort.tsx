import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { World } from "./scene/World";
import { TOTAL } from "./story";
export const PisaShort: React.FC = () => <AbsoluteFill style={{background:"#83b7e7"}}>
  <ThreeCanvas width={1080} height={1920} camera={{position:[0,9,35],fov:42,near:0.1,far:1200}} gl={{antialias:true, powerPreference:"high-performance"}}>
    <World />
  </ThreeCanvas>
  <Audio src={staticFile("audio/final-mix.wav")} />
</AbsoluteFill>;
