import { Stage, Layer, Text, Rect, Image } from "react-konva";
import useImage from "use-image";
import { useEffect, useRef, forwardRef } from "react";
import Konva from "konva";
import { useContainerSize } from "./ResizableContainer";
import { imageUrl } from "../config";

type Size = {
    width: number;
    height: number;
};
type SpriteWalkingProps = {
    width: number;
    height: number;
    src: string;
    size: Size;
};

const URLImage = forwardRef<
    Konva.Image,
    { src: string; x?: number; y?: number; width?: number; height?: number }
>(({ src, ...rest }, ref) => {
    const [image] = useImage(src, "anonymous");
    return <Image ref={ref} image={image} {...rest} />;
});

export function SpriteWalking({
    width: BASE_W,
    height: BASE_H,
    src,
    size,
}: SpriteWalkingProps) {
    const imageRef = useRef<Konva.Image>(null);
    // sprite sheet: 2x2 frames on a 1024x1024 image
    const scale = Math.min(size.width / BASE_W, size.height / BASE_H) || 1;

    const stageWidth = BASE_W * scale;
    const stageHeight = BASE_H * scale;

    const frameCols = 2;
    const frameRows = 2;
    const sheetSize = 1024;
    const spriteWidth = sheetSize / frameCols;
    const spriteHeight = sheetSize / frameRows;

    useEffect(() => {
        if (!imageRef.current) return;
        let ix = 0;
        let iy = 0;
        let gameFrame = 0;
        const staggerFrame = 30;

        const anim = new Konva.Animation((frame) => {
            const img = imageRef.current;
            if (!img) return;

            if (gameFrame % staggerFrame === 0) {
                // simple 2x2 walk cycle
                if (iy === 0 && ix === 0) ix++;
                else if (iy === 0 && ix >= frameCols - 1) {
                    ix = 0;
                    iy++;
                } else if (iy >= frameRows - 1 && ix === 0) ix++;
                else {
                    ix = 0;
                    iy = 0;
                }
            }

            imageRef.current.crop({
                x: ix * spriteWidth,
                y: iy * spriteHeight,
                width: spriteWidth,
                height: spriteHeight,
            });

            // Maintain a square
            const maxSize = Math.max(BASE_W, BASE_H);
            img.width(maxSize);
            img.height(maxSize);

            gameFrame++;
        }, imageRef.current.getLayer());

        anim.start();

        return () => {
            anim.stop();
        };
    }, [BASE_W, BASE_H, spriteHeight, spriteWidth]);

    return (
        <Stage
            width={stageWidth}
            height={stageHeight}
            scaleX={scale}
            scaleY={scale}
            className="flex items-center justify-center"
        >
            <Layer>
                <URLImage ref={imageRef} src={imageUrl("/images/"+src)} />
            </Layer>
        </Stage>
    );
}
