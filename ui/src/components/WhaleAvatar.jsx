// components/WhaleAvatar.jsx

import { useEffect, useState } from "react";

import baby1 from "../assets/baby_baekgyeong1.png";
import baby2 from "../assets/baby_baekgyeong2.png";
import babySleep from "../assets/baby_baekgyeong_sleep.png";

import child1 from "../assets/child_baekgyeong1.png";
import child2 from "../assets/child_baekgyeong2.png";
import childSleep from "../assets/child_baekgyeong_sleep.png";

import adult1 from "../assets/adult_baekgyeong1.png";
import adult2 from "../assets/adult_baekgyeong2.png";
import adultSleep from "../assets/adult_baekgyeong_sleep.png";
import "../styles/WhaleAvatar.css";

export default function WhaleAvatar({
    growthStage,
    isSleeping
}) {

    const [blink, setBlink] =
        useState(false);

    useEffect(() => {

        if (isSleeping) return;

        const interval =
            setInterval(() => {

                setBlink(true);

                setTimeout(() => {

                    setBlink(false);

                }, 250);

            }, 3000);

        return () =>
            clearInterval(interval);

    }, [isSleeping]);

    const spriteMap = {

        BABY: {
            open: baby1,
            close: baby2,
            sleep: babySleep
        },

        CHILD: {
            open: child1,
            close: child2,
            sleep: childSleep
        },

        ADULT: {
            open: adult1,
            close: adult2,
            sleep: adultSleep
        }
    };

    const current =
        spriteMap[growthStage] ||
        spriteMap.BABY;

    let imageSrc;

    if (isSleeping) {

        imageSrc = current.sleep;

    } else {

        imageSrc =
            blink
                ? current.close
                : current.open;
    }

    return (

        <img
            src={imageSrc}
            alt="Baekgyeong"
            className={
                isSleeping
                    ? "whale-sprite sleeping"
                    : "whale-sprite floating"
            }
        />

    );
}