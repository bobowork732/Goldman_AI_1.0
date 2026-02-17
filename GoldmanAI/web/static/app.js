const button = document.getElementById("generateBtn");
const resultEl = document.getElementById("result");
const videoPreview = document.getElementById("videoPreview");
const audioPreview = document.getElementById("audioPreview");
const downloadVideo = document.getElementById("downloadVideo");
const downloadAudio = document.getElementById("downloadAudio");
const downloadMix = document.getElementById("downloadMix");
const previewHint = document.getElementById("previewHint");

function resetPreview() {
  videoPreview.removeAttribute("src");
  videoPreview.load();
  audioPreview.removeAttribute("src");
  audioPreview.load();
  downloadVideo.removeAttribute("href");
  downloadAudio.removeAttribute("href");
  downloadMix.removeAttribute("href");
  previewHint.textContent = "Generate content to preview and download files.";
}

async function generate() {
  const prompt = document.getElementById("prompt").value.trim();
  const source_image = document.getElementById("sourceImage").value.trim();
  const parental_education_mode = document.getElementById("parentalMode").checked;
  const duration_seconds = Number(document.getElementById("duration").value);
  const audio_enabled = document.getElementById("audioSwitch").checked;
  const multi_shot_enabled = document.getElementById("multiShotSwitch").checked;
  const lip_sync_enabled = document.getElementById("lipSyncSwitch").checked;
  const lip_sync_focus = document.getElementById("lipSyncFocusSwitch").checked;

  if (!prompt) {
    resultEl.textContent = "Please enter a prompt.";
    return;
  }

  resultEl.textContent = "Generating...";
  resetPreview();

  try {
    const resp = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        source_image,
        parental_education_mode,
        duration_seconds,
        audio_enabled,
        multi_shot_enabled,
        lip_sync_enabled,
        lip_sync_focus,
      }),
    });

    const data = await resp.json();
    if (!resp.ok) {
      resultEl.textContent = `Error: ${data.error || "Unknown error"}`;
      return;
    }

    resultEl.textContent = JSON.stringify(data, null, 2);

    if (data.video_url) {
      videoPreview.src = data.video_url;
      videoPreview.load();
      downloadVideo.href = data.video_url;
      downloadVideo.setAttribute("download", "generated_video.mp4");
    }

    if (data.audio_url) {
      audioPreview.src = data.audio_url;
      audioPreview.load();
      downloadAudio.href = data.audio_url;
      downloadAudio.setAttribute("download", "generated_audio.wav");
      audioPreview.style.display = "block";
      downloadAudio.style.display = "inline-block";
    } else {
      audioPreview.style.display = "none";
      downloadAudio.style.display = "none";
    }

    if (data.mix_url) {
      downloadMix.href = data.mix_url;
      downloadMix.setAttribute("download", "generated_mix.txt");
    }

    previewHint.textContent = `Generated ${data.duration_seconds}s video | audio ${data.audio_enabled ? "on" : "off"} | multi-shot ${data.multi_shot_enabled ? "on" : "off"} | lip-sync ${data.lip_sync_enabled ? "on" : "off"}${data.lip_sync_focus ? " (focus)" : ""}.`;
  } catch (error) {
    resultEl.textContent = `Request failed: ${error}`;
  }
}

button?.addEventListener("click", generate);
