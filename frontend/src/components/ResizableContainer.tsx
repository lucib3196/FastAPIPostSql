import { useEffect, useRef, useState } from "react";


export function useContainerSize<T extends HTMLElement>() {
    const ref = useRef<T | null>(null);
    const [size, setSize] = useState({ width: 1000, height: 1000 });

    useEffect(() => {
        if (!ref.current) return;
        const el = ref.current;

        const ro = new ResizeObserver((entries) => {
            for (const entry of entries) {
                const cr = entry.contentRect;
                setSize({ width: cr.width, height: cr.height });
            }
        });
        ro.observe(el);
        // initialize immediately
        const rect = el.getBoundingClientRect();
        setSize({ width: rect.width, height: rect.height });

        return () => ro.disconnect();
    }, []);

    return { ref, size };
}
