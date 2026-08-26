import { useState } from "react";
import axios from "axios";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";


function App() {

  const [text, setText] = useState("");

  const [research, setResearch] = useState("");

  const [code, setCode] = useState("");

  const [review, setReview] = useState("");

  const [loading, setLoading] = useState(false);

  const [activeTab, setActiveTab] = useState("code");

  // NEW: optimization settings
  const [complexity, setComplexity] = useState("auto");

  const [reviewRequested, setReviewRequested] = useState(false);


  // SAFE STREAM FUNCTION
  const streamText = (text = "", setter) => {

    if (!text) {
      setter("No response received");
      return;
    }

    setter("");

    let index = 0;

    const interval = setInterval(() => {

      setter((prev) => prev + text[index]);

      index++;

      if (index >= text.length) {
        clearInterval(interval);
      }

    }, 1);
  };


  // RUN AI
  const runAI = async () => {

    if (!text.trim()) {
      alert("Please describe your project first.");
      return;
    }

    try {

      setLoading(true);

      setResearch("");

      setCode("");

      setReview("");


      const response = await axios.post(
        "http://127.0.0.1:8000/run-company",
        {
          project_request: text,
          complexity: complexity,
          review: reviewRequested
        }
      );


      console.log(response.data);


      // Research
      streamText(
        response.data?.research || "",
        setResearch
      );


      // Generated code
      streamText(
        response.data?.code || "",
        setCode
      );


      // Manager review
      streamText(
        response.data?.manager_review ||
        response.data?.review ||
        "",
        setReview
      );


    } catch (error) {

      console.error(error);

      setResearch("Error generating research");

      setCode("Error generating code");

      setReview("Error generating review");


    } finally {

      setLoading(false);

    }
  };


  // COPY CODE
  const copyCode = () => {

    navigator.clipboard.writeText(code);

    alert("Code copied!");

  };


  // TAB STYLE
  const tabStyle = (active) => ({
    padding: "12px 24px",

    borderRadius: "14px",

    border: active
      ? "1px solid #3b82f6"
      : "1px solid rgba(255,255,255,0.08)",

    cursor: "pointer",

    background: active
      ? "linear-gradient(135deg,#2563eb,#3b82f6)"
      : "rgba(255,255,255,0.04)",

    color: "white",

    fontWeight: "600",

    transition: "0.3s"
  });


  // CARD STYLE
  const cardStyle = {
    background: "rgba(255,255,255,0.04)",

    padding: "18px",

    borderRadius: "18px",

    border: "1px solid rgba(255,255,255,0.06)"
  };


  return (

    <div
      style={{
        minHeight: "100vh",

        display: "flex",

        background:
          "linear-gradient(135deg,#020617,#0f172a,#111827)",

        color: "white",

        fontFamily: "Arial"
      }}
    >

      {/* SIDEBAR */}

      <div
        style={{
          width: "320px",

          background: "rgba(15,23,42,0.85)",

          backdropFilter: "blur(20px)",

          borderRight:
            "1px solid rgba(255,255,255,0.08)",

          padding: "30px",

          display: "flex",

          flexDirection: "column",

          justifyContent: "space-between"
        }}
      >

        <div>

          <h1
            style={{
              fontSize: "34px",

              fontWeight: "bold",

              marginBottom: "12px",

              background:
                "linear-gradient(to right,#ffffff,#60a5fa)",

              WebkitBackgroundClip: "text",

              WebkitTextFillColor: "transparent"
            }}
          >
            AI Company
          </h1>


          <p
            style={{
              color: "#94a3b8",

              lineHeight: "1.7",

              marginBottom: "40px"
            }}
          >
            Multi-Agent Software Engineering Platform
          </p>


          {/* DASHBOARD */}

          <h2
            style={{
              marginBottom: "20px",

              fontSize: "20px"
            }}
          >
            📊 Agent Dashboard
          </h2>


          <div
            style={{
              display: "flex",

              flexDirection: "column",

              gap: "18px"
            }}
          >

            {/* RESEARCH */}

            <div style={cardStyle}>

              <h3>🧠 Research Agent</h3>

              <p style={{ color: "#94a3b8" }}>
                Status: 🟢 Active
              </p>

              <p style={{ color: "#94a3b8" }}>
                Tasks Completed: 24
              </p>


              <div
                style={{
                  height: "8px",

                  background: "#1e293b",

                  borderRadius: "10px",

                  overflow: "hidden",

                  marginTop: "12px"
                }}
              >

                <div
                  style={{
                    width: "88%",

                    height: "100%",

                    background: "#22c55e"
                  }}
                />

              </div>

            </div>


            {/* CODING */}

            <div style={cardStyle}>

              <h3>💻 Coding Agent</h3>

              <p style={{ color: "#94a3b8" }}>
                Status: 🟢 Running
              </p>

              <p style={{ color: "#94a3b8" }}>
                Code Accuracy: 94%
              </p>


              <div
                style={{
                  height: "8px",

                  background: "#1e293b",

                  borderRadius: "10px",

                  overflow: "hidden",

                  marginTop: "12px"
                }}
              >

                <div
                  style={{
                    width: "94%",

                    height: "100%",

                    background: "#3b82f6"
                  }}
                />

              </div>

            </div>


            {/* MANAGER */}

            <div style={cardStyle}>

              <h3>📋 Manager Agent</h3>

              <p style={{ color: "#94a3b8" }}>
                Status: 🟢 Reviewing
              </p>

              <p style={{ color: "#94a3b8" }}>
                Approval Rate: 97%
              </p>


              <div
                style={{
                  height: "8px",

                  background: "#1e293b",

                  borderRadius: "10px",

                  overflow: "hidden",

                  marginTop: "12px"
                }}
              >

                <div
                  style={{
                    width: "97%",

                    height: "100%",

                    background: "#a855f7"
                  }}
                />

              </div>

            </div>

          </div>

        </div>


        {/* FOOTER */}

        <div
          style={{
            color: "#64748b",

            fontSize: "14px",

            marginTop: "40px"
          }}
        >
          AI Software Company v2
        </div>

      </div>


      {/* MAIN CONTENT */}

      <div
        style={{
          flex: 1,

          padding: "40px"
        }}
      >

        {/* HEADER */}

        <div
          style={{
            marginBottom: "35px"
          }}
        >

          <h1
            style={{
              fontSize: "52px",

              marginBottom: "10px",

              fontWeight: "bold"
            }}
          >
            Build Software with AI
          </h1>


          <p
            style={{
              color: "#94a3b8",

              fontSize: "18px"
            }}
          >
            Describe your project idea and let AI agents build it.
          </p>

        </div>


        {/* INPUT */}

        <div
          style={{
            background: "rgba(15,23,42,0.75)",

            backdropFilter: "blur(20px)",

            border:
              "1px solid rgba(255,255,255,0.08)",

            borderRadius: "24px",

            padding: "30px",

            marginBottom: "30px"
          }}
        >

          <textarea
            rows="5"

            value={text}

            onChange={(e) => setText(e.target.value)}

            placeholder="Example: Build a calculator app with beautiful UI..."

            style={{
              width: "100%",

              background: "transparent",

              color: "white",

              border: "none",

              outline: "none",

              resize: "none",

              fontSize: "17px",

              lineHeight: "1.8"
            }}
          />


          {/* OPTIMIZATION CONTROLS */}

          <div
            style={{
              display: "flex",

              gap: "20px",

              alignItems: "center",

              flexWrap: "wrap",

              marginTop: "20px"
            }}
          >

            {/* COMPLEXITY */}

            <label
              style={{
                color: "#94a3b8"
              }}
            >

              Mode:

              <select
                value={complexity}

                onChange={(e) =>
                  setComplexity(e.target.value)
                }

                style={{
                  marginLeft: "8px",

                  padding: "8px 12px",

                  borderRadius: "10px",

                  background: "#0f172a",

                  color: "white",

                  border:
                    "1px solid rgba(255,255,255,0.12)"
                }}
              >

                <option value="auto">
                  Auto
                </option>

                <option value="simple">
                  Simple — 1 AI call
                </option>

                <option value="complex">
                  Complex — Research + Coding
                </option>

              </select>

            </label>


            {/* MANAGER REVIEW */}

            <label
              style={{
                color: "#94a3b8",

                cursor: "pointer"
              }}
            >

              <input
                type="checkbox"

                checked={reviewRequested}

                onChange={(e) =>
                  setReviewRequested(
                    e.target.checked
                  )
                }

                style={{
                  marginRight: "8px"
                }}
              />

              Request manager review

            </label>

          </div>


          {/* GENERATE BUTTON */}

          <div
            style={{
              display: "flex",

              justifyContent: "space-between",

              alignItems: "center",

              marginTop: "25px"
            }}
          >

            <button
              onClick={runAI}

              disabled={loading}

              style={{
                background:
                  loading
                    ? "#334155"
                    : "linear-gradient(135deg,#2563eb,#3b82f6)",

                color: "white",

                border: "none",

                padding: "16px 28px",

                borderRadius: "16px",

                cursor: "pointer",

                fontSize: "16px",

                fontWeight: "bold"
              }}
            >

              {loading
                ? "⚡ AI Agents Working..."
                : "🚀 Generate Software"}

            </button>


            <div
              style={{
                color:
                  loading
                    ? "#38bdf8"
                    : "#22c55e",

                fontWeight: "bold"
              }}
            >

              {loading
                ? "Processing Request..."
                : "System Ready"}

            </div>

          </div>

        </div>


        {/* TABS */}

        <div
          style={{
            display: "flex",

            gap: "12px",

            marginBottom: "25px"
          }}
        >

          <button
            onClick={() =>
              setActiveTab("research")
            }

            style={tabStyle(
              activeTab === "research"
            )}
          >
            🔍 Research
          </button>


          <button
            onClick={() =>
              setActiveTab("code")
            }

            style={tabStyle(
              activeTab === "code"
            )}
          >
            💻 Code
          </button>


          <button
            onClick={() =>
              setActiveTab("review")
            }

            style={tabStyle(
              activeTab === "review"
            )}
          >
            📋 Review
          </button>

        </div>


        {/* OUTPUT */}

        <div
          style={{
            background: "rgba(15,23,42,0.75)",

            backdropFilter: "blur(20px)",

            border:
              "1px solid rgba(255,255,255,0.08)",

            borderRadius: "24px",

            padding: "30px",

            minHeight: "500px"
          }}
        >

          {/* RESEARCH */}

          {activeTab === "research" && (

            <pre
              style={{
                whiteSpace: "pre-wrap",

                lineHeight: "1.8",

                color: "#e2e8f0"
              }}
            >
              {research}
            </pre>

          )}


          {/* CODE */}

          {activeTab === "code" && (

            <div>

              <div
                style={{
                  display: "flex",

                  justifyContent: "space-between",

                  alignItems: "center",

                  marginBottom: "20px"
                }}
              >

                <h2>
                  💻 Generated Code
                </h2>


                <button
                  onClick={copyCode}

                  style={{
                    background:
                      "linear-gradient(135deg,#2563eb,#3b82f6)",

                    color: "white",

                    border: "none",

                    padding: "10px 18px",

                    borderRadius: "12px",

                    cursor: "pointer"
                  }}
                >
                  Copy Code
                </button>

              </div>


              <SyntaxHighlighter
                language="python"

                style={oneDark}
              >
                {code || "No code generated yet"}
              </SyntaxHighlighter>

            </div>

          )}


          {/* REVIEW */}

          {activeTab === "review" && (

            <pre
              style={{
                whiteSpace: "pre-wrap",

                lineHeight: "1.8",

                color: "#e2e8f0"
              }}
            >
              {review}
            </pre>

          )}

        </div>

      </div>

    </div>
  );
}


export default App;