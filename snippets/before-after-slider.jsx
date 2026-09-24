export const BeforeAfterSlider = ({
  before,
  after,
  beforeAlt,
  afterAlt,
  width,
  height,
  caption,
  beforeLabel = "Before",
  afterLabel = "After",
  sliderLabel = "Drag to compare before and after",
}) => {
  const [position, setPosition] = useState(50);

  const label = {
    position: "absolute",
    top: 12,
    padding: "4px 10px",
    borderRadius: 9999,
    background: "rgba(17, 24, 39, 0.75)",
    color: "#fff",
    fontSize: 12,
    fontWeight: 600,
    lineHeight: "16px",
    pointerEvents: "none",
  };

  return (
    <figure style={{ margin: "1.5rem 0" }}>
      <div
        style={{
          position: "relative",
          overflow: "hidden",
          borderRadius: 12,
          border: "1px solid rgba(128, 128, 128, 0.25)",
          aspectRatio: `${width} / ${height}`,
          userSelect: "none",
        }}
      >
        <img
          src={after}
          alt={afterAlt}
          width={width}
          height={height}
          noZoom
          draggable={false}
          style={{ display: "block", width: "100%", height: "100%", margin: 0 }}
        />

        <img
          src={before}
          alt={beforeAlt}
          width={width}
          height={height}
          noZoom
          draggable={false}
          style={{
            position: "absolute",
            inset: 0,
            display: "block",
            width: "100%",
            height: "100%",
            margin: 0,
            clipPath: `inset(0 ${100 - position}% 0 0)`,
          }}
        />

        <span style={{ ...label, left: 12, opacity: position > 12 ? 1 : 0 }}>
          {beforeLabel}
        </span>
        <span style={{ ...label, right: 12, opacity: position < 88 ? 1 : 0 }}>
          {afterLabel}
        </span>

        <div
          aria-hidden="true"
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: `${position}%`,
            width: 3,
            marginLeft: -1.5,
            background: "#fff",
            boxShadow: "0 0 0 1px rgba(17, 24, 39, 0.2)",
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              width: 40,
              height: 40,
              marginTop: -20,
              marginLeft: -20,
              borderRadius: 9999,
              background: "#fff",
              boxShadow: "0 2px 8px rgba(17, 24, 39, 0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#0f766e",
              fontSize: 16,
              fontWeight: 700,
            }}
          >
            ⟷
          </div>
        </div>

        <input
          type="range"
          min={0}
          max={100}
          step={1}
          value={position}
          aria-label={sliderLabel}
          aria-valuetext={`${position}% ${beforeLabel.toLowerCase()}`}
          onChange={(event) => setPosition(Number(event.target.value))}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            margin: 0,
            opacity: 0,
            cursor: "ew-resize",
          }}
        />
      </div>

      {caption ? (
        <figcaption
          style={{ marginTop: 8, fontSize: 14, textAlign: "center", opacity: 0.75 }}
        >
          {caption}
        </figcaption>
      ) : null}
    </figure>
  );
};
