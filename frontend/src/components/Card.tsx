
import { motion } from "motion/react";


const variants = {
    front: { rotateY: 0 },
    back: { rotateY: 180 },
    reset: { x: 0, y: 0 },
};

type CardProps = {
    color: string;
    style?: React.CSSProperties
    imgUrl?: string
}
type CardImageProps = {
    imgUrl: string
}
const CardImage = ({ imgUrl }: CardImageProps) => {
    return (
        <div className="w-full h-full" style={{
            backgroundImage: `url("${imgUrl}")`,
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
            backgroundPosition: "center",
        }}>

        </div>)
}

const Card: React.FC<CardProps> = ({ color, style, imgUrl }) => {
    return (
        <motion.div
            variants={variants}
            dragConstraints={{ left: -500, right: 300, top: 0, bottom: 300 }}
            className={`flex flex-col w-[300px] h-[400px] rounded-2xl ${color} shadow-lg transform-gpu drop-shadow-lg `}
            style={style}
        >
            <CardImage imgUrl={imgUrl} />
        </motion.div>
    );
};

export default Card