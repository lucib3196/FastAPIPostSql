import { SpriteWalking } from "./SpriteAnimation";
import { useState, useEffect } from "react";
import type { MonsterData } from "./ViewIndividualMonster";
import { useContainerSize } from "./ResizableContainer";
import { SplitFileNames } from "../utils";
import { GetPokemonFiles } from "../api/monsterServices";

function MonsterAllAnimations() {
    const [monsterData, setMonsterData] = useState<MonsterData[]>([]);

    useEffect(() => {
        const getMonster = async () => {
            const monsterAnimation = await GetPokemonFiles(32, "animations");
            const data = SplitFileNames(monsterAnimation);
            setMonsterData(data);
        };
        getMonster();
    }, []);

    return (
        <div className="flex flex-wrap items-center justify-center gap-8 p-6 bg-gray-900/40 rounded-2xl shadow-lg">
            {monsterData.map((val, id) => (
                <IndividualMonsterContainer key={id} src={val.image_path} />
            ))}
        </div>
    );
}

type IndividualProps = {
    src: string;
};

function IndividualMonsterContainer({ src }: IndividualProps) {
    const { ref: containerRef, size } = useContainerSize<HTMLDivElement>();

    return (
        <div
            ref={containerRef}
            className="flex items-center justify-center w-40 h-40 rounded-xl border border-gray-700 bg-gray-800 hover:scale-105 transition-transform duration-200 shadow-md"
        >
            <SpriteWalking width={100} height={100} src={src} size={size} />
        </div>
    );
}

export default function ViewAllMonster() {
    return (
        <section className="p-8">
            <h1 className="mb-6 text-2xl font-bold text-center text-white">
                All Animations
            </h1>
            <MonsterAllAnimations />
        </section>
    );
}
