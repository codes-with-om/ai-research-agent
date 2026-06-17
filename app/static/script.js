const chatBox = document.getElementById("chatBox");
const queryInput = document.getElementById("queryInput");
const sendBtn = document.getElementById("sendBtn");
const statusBadge = document.getElementById("statusBadge");
const newChatBtn = document.getElementById("newChatBtn");
const hintChips = document.querySelectorAll(".hint-chip");
let userName = localStorage.getItem("userName") || "";

function getInitials(name) {
  return name
    .trim()
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function updateUserUI() {
  const nameElement = document.querySelector(".user-name");
  const avatarElement = document.querySelector(".avatar");
  const welcomeMessage = document.getElementById("welcomeMessage");

  const displayName = userName || "Guest User";

  if (nameElement) {
    nameElement.innerText = displayName;
  }

  if (avatarElement) {
    avatarElement.innerText = getInitials(displayName);
  }

  if (welcomeMessage) {
    welcomeMessage.innerText = `Hi ${displayName} 👋 Ask me anything. I can research or write depending on your query.`;
  }
}

async function askUserNameIfNeeded() {
  if (userName) {
    updateUserUI();
    return;
  }

  const result = await Swal.fire({
    title: "Welcome 👋",
    text: "What should I call you?",
    input: "text",
    inputPlaceholder: "Enter your name",
    background: "#282a36",
    color: "#f8f8f2",
    confirmButtonColor: "#bd93f9",
    allowOutsideClick: false,
    inputValidator: (value) => {
      if (!value.trim()) {
        return "Please enter your name";
      }
    },
  });

  userName = result.value.trim();
  localStorage.setItem("userName", userName);
  updateUserUI();
}

function setStatus(text, type = "ready") {
  statusBadge.innerHTML = `<span class="status-dot"></span>${text}`;

  if (type === "ready") {
    statusBadge.style.color = "var(--drac-green)";
    statusBadge.style.borderColor = "rgba(80, 250, 123, 0.27)";
    statusBadge.style.background = "rgba(80, 250, 123, 0.08)";
  }

  if (type === "thinking") {
    statusBadge.style.color = "var(--drac-yellow)";
    statusBadge.style.borderColor = "rgba(241, 250, 140, 0.27)";
    statusBadge.style.background = "rgba(241, 250, 140, 0.08)";
  }

  if (type === "error") {
    statusBadge.style.color = "var(--drac-red)";
    statusBadge.style.borderColor = "rgba(255, 85, 85, 0.27)";
    statusBadge.style.background = "rgba(255, 85, 85, 0.08)";
  }
}

function formatSourceTitle(sourceText, index) {
  const titleLine = sourceText
    .split("\n")
    .find((line) => line.toLowerCase().startsWith("title:"));

  if (!titleLine) {
    return `Source ${index + 1}`;
  }

  return titleLine.replace("Title:", "").trim();
}

function extractSourceUrl(sourceText) {
  const urlLine = sourceText
    .split("\n")
    .find((line) => line.toLowerCase().startsWith("url:"));

  if (!urlLine) {
    return "#";
  }

  return urlLine.replace("URL:", "").trim();
}

function addMessage(content, type = "bot", meta = "", sources = []) {
  const row = document.createElement("div");
  row.className = `msg-row ${type}`;

  const avatar = document.createElement("div");
  avatar.className = `msg-avatar ${type}`;
  avatar.innerText = type === "user" ? getInitials(userName || "User") : "AI";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  if (content) {
    if (type === "bot") {
      bubble.innerHTML = marked.parse(content);
    } else {
      bubble.innerText = content;
    }
  }

  if (meta) {
    const metaDiv = document.createElement("div");
    metaDiv.className = "msg-meta";
    metaDiv.innerText = meta;
    bubble.appendChild(metaDiv);
  }

  if (sources && sources.length > 0) {
    const sourcesRow = document.createElement("div");
    sourcesRow.className = "sources-row";

    sources.forEach((source, index) => {
      const chip = document.createElement("a");
      chip.className = "source-chip";
      chip.innerText = `🔗 ${formatSourceTitle(source, index)}`;
      chip.href = extractSourceUrl(source);
      chip.target = "_blank";
      chip.rel = "noopener noreferrer";
      chip.title = source;
      sourcesRow.appendChild(chip);
    });

    bubble.appendChild(sourcesRow);
  }

  row.appendChild(avatar);
  row.appendChild(bubble);

  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;

  return row;
}

function typeText(element, text, speed = 8) {
  return new Promise((resolve) => {
    let index = 0;

    function type() {
      if (index < text.length) {
        element.innerText += text.charAt(index);
        index++;
        chatBox.scrollTop = chatBox.scrollHeight;
        setTimeout(type, speed);
      } else {
        resolve();
      }
    }

    type();
  });
}

function addLoader() {
  const row = document.createElement("div");
  row.className = "msg-row bot";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar bot";
  avatar.innerText = "AI";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";

  const loader = document.createElement("div");
  loader.className = "loader";
  loader.innerHTML = "<span></span><span></span><span></span>";

  bubble.appendChild(loader);
  row.appendChild(avatar);
  row.appendChild(bubble);

  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;

  return row;
}

async function sendQuery() {
  const query = queryInput.value.trim();

  if (!query) {
    Swal.fire({
      icon: "warning",
      title: "Empty query",
      text: "Please enter a question first.",
      background: "#282a36",
      color: "#f8f8f2",
      confirmButtonColor: "#bd93f9",
    });
    return;
  }

  addMessage(query, "user");
  queryInput.value = "";

  sendBtn.disabled = true;
  setStatus("Thinking...", "thinking");

  const loader = addLoader();

  try {
    const response = await fetch("/research", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    loader.remove();

    if (!response.ok || data.status === "failed") {
      Swal.fire({
        icon: "error",
        title: "Request failed",
        text: data.message || "Something went wrong.",
        background: "#282a36",
        color: "#f8f8f2",
        confirmButtonColor: "#ff5555",
      });

      setStatus("Error", "error");
      return;
    }

    const meta = `Path: ${data.execution_path} · Time: ${data.execution_time}s`;

    const botMessage = addMessage("", "bot");

    const bubble = botMessage.querySelector(".msg-bubble");
    
    bubble.innerHTML = marked.parse(data.message);  

    if (meta) {
      const metaDiv = document.createElement("div");
      metaDiv.className = "msg-meta";
      metaDiv.innerText = meta;
      bubble.appendChild(metaDiv);
    }

    if (data.sources && data.sources.length > 0) {
      const sourcesRow = document.createElement("div");
      sourcesRow.className = "sources-row";

      data.sources.forEach((source, index) => {
        const chip = document.createElement("a");

        chip.className = "source-chip";
        chip.innerText = `🔗 ${formatSourceTitle(source, index)}`;

        chip.href = extractSourceUrl(source);
        chip.target = "_blank";
        chip.rel = "noopener noreferrer";

        chip.title = source;

        sourcesRow.appendChild(chip);
      });
      bubble.appendChild(sourcesRow);
    }

    setStatus("Ready", "ready");
  } catch (error) {
    loader.remove();

    Swal.fire({
      icon: "error",
      title: "Server error",
      text: "Could not connect to the backend.",
      background: "#282a36",
      color: "#f8f8f2",
      confirmButtonColor: "#ff5555",
    });

    setStatus("Error", "error");
  } finally {
    sendBtn.disabled = false;
    queryInput.focus();
  }
}

sendBtn.addEventListener("click", sendQuery);

queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendQuery();
  }
});

newChatBtn.addEventListener("click", () => {
  chatBox.innerHTML = "";
  addMessage(
    `New chat started. Ask me anything, ${userName || "there"} 👋`,
    "bot",
  );
  setStatus("Ready", "ready");
  queryInput.focus();
});

hintChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    queryInput.value = chip.innerText;
    queryInput.focus();
  });
});

askUserNameIfNeeded();