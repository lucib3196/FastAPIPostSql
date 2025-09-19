import React, { useRef, useState, useEffect } from "react";
import { SpriteWalking } from "./SpriteAnimation";
import { GetPokemonFiles } from "../api/monsterServices";
import { SplitFileNames } from "../utils";
import { Dropdown } from "./DropDown";
import { useContainerSize } from "./ResizableContainer";

export type MonsterData = {
    name: string;
    image_path: string;
};
// Todo remove the hardcoded 2

export function ViewIndividualMonster() {
    const [monsterData, setMonsterData] = useState<MonsterData[]>([]);
    const [selectedAnimation, setSelectedAnimation] = useState("");
    const { ref: containerRef, size } = useContainerSize<HTMLDivElement>();
    useEffect(() => {
        const getMonster = async () => {
            const monsterAnimation = await GetPokemonFiles(36, "animations");
            const data = SplitFileNames(monsterAnimation);
            setMonsterData(data);

            if (data.length && !selectedAnimation) {
                setSelectedAnimation(data[0].name);
            }
        };
        getMonster();
    }, []);
    
    const animationNames = monsterData.map((val) => val.name);
    console.log(animationNames)
    const srcObj = monsterData.find(
        (v) => v.name.toLowerCase() === selectedAnimation.toLowerCase()
    );
    const src = srcObj?.image_path;
    return (
        <div ref={containerRef} className="md:w-1/2 md:h-1/2 w-full h-full flex flex-col justify-center items-center border rounded-lg overflow-hidden">
            <div>
                <SpriteWalking width={100} src={src} height={100} size={size} />
            </div>
            <Dropdown
                animations={animationNames}
                selectedAnimation={selectedAnimation}
                onChange={setSelectedAnimation}
            />
        </div>
    );
}



