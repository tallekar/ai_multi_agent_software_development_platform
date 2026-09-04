import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark, oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [text, setText] = useState("");
  const [research, setResearch] = useState("");
  const [architecture, setArchitecture] = useState("");
  const [code, setCode] = useState("");
  const [testing, setTesting] = useState("");
  const [debugging, setDebugging] = useState("");
  const [codeReview, setCodeReview] = useState("");
  const [validation, setValidation] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("code");

  // Optimization settings
  const [complexity, setComplexity] = useState("auto");
  const [reviewRequested, setReviewRequested] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [projectName, setProjectName] = useState("");

  // Theme state: 'dark' | 'light'
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "dark";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

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
      setArchitecture("");
      setCode("");
      setTesting("");
      setDebugging("");
      setCodeReview("");
      setValidation(null);
      setRetryCount(0);
      setReview("");
      setDownloadUrl("");
      setProjectName("");

      const response = await axios.post("http://127.0.0.1:8000/run-company", {
        project_request: text,
        complexity: complexity,
        review: reviewRequested
      });

      const project = response.data?.project || {};
      setDownloadUrl(
        response.data?.download_url ||
          project.download_url ||
          (project.project_id
            ? `/projects/${project.project_id}/download`
            : "")
      );
      setProjectName(
        response.data?.project_name ||
          project.project_name ||
          project.project_id ||
          "generated-project"
      );

      streamText(response.data?.research || "", setResearch);
      streamText(response.data?.architecture || "", setArchitecture);
      streamText(response.data?.code || "", setCode);
      streamText(response.data?.testing || "", setTesting);
      streamText(response.data?.debugging || "", setDebugging);
      streamText(response.data?.code_review || "", setCodeReview);
      setValidation(response.data?.validation || null);
      setRetryCount(response.data?.retry_count || 0);
      streamText(
        response.data?.manager_review || response.data?.review || "",
        setReview
      );
    } catch (error) {
      console.error(error);
      setResearch("Error generating research");
      setArchitecture("Error generating architecture");
      setCode("Error generating code");
      setTesting("Error generating testing result");
      setDebugging("Error generating debugging result");
      setCodeReview("Error generating code review");
      setValidation(null);
      setReview("Error generating review");
    } finally {
      setLoading(false);
    }
  };

  const copyCode = () => {
    navigator.clipboard.writeText(code);
    alert("Code copied!");
  };

  const tabs = [
    { id: "research", label: "Research", icon: "🔍" },
    { id: "architecture", label: "Architecture", icon: "🏗️" },
    { id: "code", label: "Code", icon: "💻" },
    { id: "testing", label: "Testing", icon: "🧪" },
    { id: "debugging", label: "Debugging", icon: "🐛" },
    { id: "code_review", label: "Code Review", icon: "🔎" },
    { id: "validation", label: "Validation", icon: "✅" },
    { id: "review", label: "Manager", icon: "📋" }
  ];

  return (
    <div className="app-shell">
      {/* SIDEBAR */}
      <aside className="app-sidebar">
        <div>
          <div className="brand-header">
            <div className="brand-title-wrap">
              <span className="brand-icon">⚡</span>
              <h1 className="brand-title">AI Company</h1>
            </div>
            <p className="brand-subtitle">
              Multi-Agent Software Engineering Platform
            </p>
          </div>

          <div className="section-header">
            <h2>📊 Agent Dashboard</h2>
          </div>

          <div className="dashboard-cards">
            {/* RESEARCH */}
            <div className="agent-card">
              <div className="agent-card-header">
                <h3>🧠 Research Agent</h3>
                <span className="status-badge status-active">Active</span>
              </div>
              <p className="agent-meta">Tasks Completed: 24</p>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: "88%", background: "var(--success)" }} />
              </div>
            </div>

            {/* CODING */}
            <div className="agent-card">
              <div className="agent-card-header">
                <h3>💻 Coding Agent</h3>
                <span className="status-badge status-active">Running</span>
              </div>
              <p className="agent-meta">Code Accuracy: 94%</p>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: "94%", background: "var(--accent-primary)" }} />
              </div>
            </div>

            {/* MANAGER */}
            <div className="agent-card">
              <div className="agent-card-header">
                <h3>📋 Manager Agent</h3>
                <span className="status-badge status-active">Reviewing</span>
              </div>
              <p className="agent-meta">Approval Rate: 97%</p>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: "97%", background: "var(--accent-purple)" }} />
              </div>
            </div>
          </div>
        </div>

        <div className="sidebar-footer">
          <span>AI Software Company v2</span>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="app-main">
        {/* HEADER */}
        <header className="app-header">
          <div>
            <h1>Build Software with AI</h1>
            <p>Describe your project idea and let autonomous agents execute it.</p>
          </div>

          <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="Toggle theme">
            {theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode"}
          </button>
        </header>

        {/* INPUT COMPOSER */}
        <section className="app-composer">
          <textarea
            rows="4"
            className="project-prompt"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="e.g., Build a responsive task management dashboard in React with drag-and-drop..."
          />

          <div className="composer-controls">
            <div className="options-group">
              <label className="select-label">
                <span>Execution Mode:</span>
                <select
                  value={complexity}
                  onChange={(e) => setComplexity(e.target.value)}
                  className="control-select"
                >
                  <option value="auto">Auto Select</option>
                  <option value="simple">Simple (Fast Code Generation)</option>
                  <option value="complex">Complex (Full Workflow Pipeline)</option>
                </select>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={reviewRequested}
                  onChange={(e) => setReviewRequested(e.target.checked)}
                />
                <span>Request Manager Review</span>
              </label>
            </div>

            <div className="action-group">
              <span className={`status-indicator ${loading ? "is-loading" : "is-ready"}`}>
                <span className="dot" />
                {loading ? "Processing Pipeline..." : "System Ready"}
              </span>

              <button
                onClick={runAI}
                disabled={loading}
                className="generate-button"
              >
                {loading ? "⚡ Agents Working..." : "🚀 Generate Software"}
              </button>
            </div>
          </div>
        </section>

        <section className={`download-section ${downloadUrl ? "is-ready" : "is-empty"}`}>
          <div>
            <h3>Download project ZIP</h3>
            <p>
              {downloadUrl
                ? `${projectName} is ready to download.`
                : "Generate software to create a downloadable ZIP file."}
            </p>
          </div>
          {downloadUrl ? (
            <a
              className="download-button"
              href={`http://127.0.0.1:8000${downloadUrl}`}
              download
            >
              Download ZIP
            </a>
          ) : (
            <span className="download-button is-disabled">Download ZIP</span>
          )}
        </section>

        {/* TABS */}
        <nav className="app-tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`tab-btn ${activeTab === tab.id ? "active" : ""}`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>

        {/* OUTPUT */}
        <section className="app-output">
          {activeTab === "research" && (
            <div className="output-content">
              <h3>🔍 Research Output</h3>
              <pre className="output-text">{research || "No research data generated yet."}</pre>
            </div>
          )}

          {activeTab === "architecture" && (
            <div className="output-content">
              <h3>🏗️ System Architecture</h3>
              <pre className="output-text">{architecture || "No architecture generated yet."}</pre>
            </div>
          )}

          {activeTab === "code" && (
            <div className="output-content">
              <div className="code-header">
                <h3>💻 Generated Source Code</h3>
                <button onClick={copyCode} className="copy-btn">
                  📋 Copy Code
                </button>
              </div>
              <div className="code-viewer-container">
                <SyntaxHighlighter
                  language="python"
                  style={theme === "dark" ? oneDark : oneLight}
                  customStyle={{
                    margin: 0,
                    borderRadius: "12px",
                    fontSize: "14px",
                    background: "var(--code-bg)"
                  }}
                >
                  {code || "# No code generated yet."}
                </SyntaxHighlighter>
              </div>
            </div>
          )}

          {activeTab === "testing" && (
            <div className="output-content">
              <h3>🧪 Test Suites & Results</h3>
              <pre className="output-text">{testing || "No testing results available."}</pre>
            </div>
          )}

          {activeTab === "debugging" && (
            <div className="output-content">
              <h3>🐛 Debugging Logs</h3>
              <pre className="output-text">{debugging || "No debugging required or logged."}</pre>
            </div>
          )}

          {activeTab === "code_review" && (
            <div className="output-content">
              <h3>🔎 Code Quality Review</h3>
              <pre className="output-text">{codeReview || "No code review generated yet."}</pre>
            </div>
          )}

          {activeTab === "validation" && (
            <div className="output-content">
              <h3>✅ Validation Status</h3>
              <div className="validation-metrics">
                <div className="metric-box">
                  <span className="metric-label">Status</span>
                  <span className="metric-value">{validation?.status || "N/A"}</span>
                </div>
                <div className="metric-box">
                  <span className="metric-label">Retry Count</span>
                  <span className="metric-value">{retryCount}</span>
                </div>
              </div>
              {validation && (
                <pre className="output-text">
                  {JSON.stringify(validation, null, 2)}
                </pre>
              )}
            </div>
          )}

          {activeTab === "review" && (
            <div className="output-content">
              <h3>📋 Manager Final Review</h3>
              <pre className="output-text">{review || "No manager review requested or available."}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;