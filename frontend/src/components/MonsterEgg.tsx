import * as motion from "motion/react-client";
import type { Variants } from "framer-motion";


const variants: Variants = {
    idle: { scaleX: 1, scaleY: 1, rotate: 0 },
    hatching: {
        scaleX: [1, 1.07, 0.95, 1.04, 1],
        scaleY: [1, 0.93, 1.07, 0.97, 1],
        rotate: [0, 1.5, -1.2, 0.6, 0],
        transition: { duration: 0.8, repeat: Infinity, ease: "easeInOut" },
    },
    growing: {
        scaleX: 1, scaleY: 1, rotate: [0, 4, -5, 6, 2, -1, 0], transition: { duration: 0.8, repeat: Infinity, ease: "easeInOut" },
    }
};

export function MonsterEgg({ canMove }: { canMove: boolean }) {
    return (
        <motion.div
            style={eggStyle}
            initial={"idle"}
            variants={variants}
            animate={canMove ? "growing" : "idle"}>
            <div style={spot("50%", "50%", "20%", "30%", "blue")} />
            <div style={spot("20%", "30%", "30%", "15%", "blue")} />
            <div style={spot("30%", "80%", "10%", "10%", "blue")} />
            <div style={spot("70%", "10%", "10%", "10%", "blue")} />
        </motion.div>
    );
}
const spot = (
    left: number | string,
    top: number | string,
    width: number | string = "10%",
    height: number | string = "10%",
    color: string = "black"
): React.CSSProperties => ({
    position: "absolute",
    width: width,
    height: height,
    backgroundColor: color,
    borderRadius: "50%",
    left,
    top,
    opacity: 0.8,
});

const eggStyle: React.CSSProperties = {
    transformOrigin: "center",
    position: "relative",
    width: 300,
    height: 300, // taller than wide → more like an egg
    backgroundColor: "white",
    borderRadius: "50% 50% 45% 45% / 55% 55% 45% 45%", // egg shape
};
