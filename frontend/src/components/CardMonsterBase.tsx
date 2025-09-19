import { SpriteWalking } from "./SpriteAnimation";
import { useState, useEffect } from "react";
import type { MonsterData } from "./ViewIndividualMonster";
import { useContainerSize } from "./ResizableContainer";
import { SplitFileNames } from "../utils";
import { GetPokemonFiles } from "../api/monsterServices";
import { imageUrl } from "../config";
import Card from "./Card";

type MonsterBaseProp = {
    monsterId: number
}


export function MonsterBaseCard({ monsterId }: MonsterBaseProp) {
    const [monsterData, setMonsterData] = useState<MonsterData[] | null>();
    const [imgUrl, setImageUrl] = useState("")
    useEffect(() => {
        const getMonster = async () => {
            try {
                const monsterAnimation = await GetPokemonFiles(monsterId, "base");
                const data = SplitFileNames(monsterAnimation);
                setMonsterData(data); // Should only return one
            } catch (error) {
                console.log(error)
            }


        };
        getMonster();
    }, []);
    useEffect(() => {
        if (!monsterData) return;
        const img = imageUrl("/images/" + monsterData[0].image_path)
        setImageUrl(img)
    }, [monsterId, monsterData])

    console.log(imgUrl)
    return <div className="flex flex-col">
        <Card
            color="bg-gray-100 border-4"
            imgUrl={imgUrl}
        />

    </div>

}

