export default function StatusPanel({ stateData }) {

    return (

        <div className="status-panel">

            <StatusBar
                label="❤️ 호감도"
                value={stateData.favorability}
            />

            <StatusBar
                label="🍖 배고픔"
                value={stateData.hunger}
            />

            <StatusBar
                label="⚡ 기력"
                value={stateData.energy}
            />

            <StatusBar
                label="🎉 재미"
                value={stateData.fun}
            />

        </div>
    );
}

function StatusBar({ label, value }) {

    return (

        <div className="status-item">

            <span>{label}</span>

            <div className="progress">

                <div
                    className="fill"
                    style={{
                        width: `${value}%`
                    }}
                />

            </div>

        </div>
    );
}