// hooks/useBlinkAnimation.js

import { useEffect, useState } from "react";

export default function useBlinkAnimation(openSprite, closeSprite) {

    const [sprite, setSprite] = useState(openSprite);

    useEffect(() => {

        const interval = setInterval(() => {

            setSprite(closeSprite);

            setTimeout(() => {
                setSprite(openSprite);
            }, 180);

        }, 3500);

        return () => clearInterval(interval);

    }, [openSprite, closeSprite]);

    return sprite;
}