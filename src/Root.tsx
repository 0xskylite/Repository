import React from "react";
import { Composition } from "remotion";
import { PisaShort } from "./PisaShort";
import { TOTAL, FPS } from "./story";
export const Root: React.FC = () => <Composition id="PisaShort" component={PisaShort} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} />;
