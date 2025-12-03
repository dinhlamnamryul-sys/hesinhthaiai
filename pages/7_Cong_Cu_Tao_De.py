const express = require("express");
const multer = require("multer");
const fs = require("fs");
const pdfParse = require("pdf-parse");
const mammoth = require("mammoth");
const axios = require("axios");
require("dotenv").config();

const upload = multer({ dest: "uploads/" });
const app = express();

async function readFileText(path, mime) {
  if (mime === "application/pdf") {
    const data = fs.readFileSync(path);
    const r = await pdfParse(data);
    return r.text;
  }

  if (mime.includes("word")) {
    const r = await mammoth.extractRawText({ path });
    return r.value;
  }

  return fs.readFileSync(path, "utf8");
}

app.post(
  "/api/generate",
  upload.fields([
    { name: "textbook" },
    { name: "document" },
    { name: "template" },
  ]),
  async (req, res) => {
    try {
      const instruction = req.body.instruction || "";
      const files = req.files;

      const tb = await readFileText(
        files.textbook[0].path,
        files.textbook[0].mimetype
      );
      const cv = await readFileText(
        files.document[0].path,
        files.document[0].mimetype
      );
      const template = await readFileText(
        files.template[0].path,
        files.template[0].mimetype
      );

      const prompt = `
Trích xuất ma trận và đề kiểm tra theo đúng mẫu.
Trả về JSON:
{
 "matrixHtml": "...",
 "examHtml": "..."
}

Nội dung sách:
${tb}

Công văn:
${cv}

Mẫu đề:
${template}

Yêu cầu của người dùng:
${instruction}
`;

      const aiResponse = await callOpenAI(prompt);
      let parsed = JSON.parse(aiResponse);

      Object.values(files).flat().forEach((f) => fs.unlinkSync(f.path));

      res.json(parsed);
    } catch (err) {
      console.error(err);
      res.status(500).send(String(err));
    }
  }
);

async function callOpenAI(prompt) {
  return JSON.stringify({
    matrixHtml:
      '<table><tr><th>Chủ đề</th><th>Số câu</th></tr><tr><td>Phép nhân</td><td>4</td></tr></table>',
    examHtml: "<h1>Đề kiểm tra mẫu</h1><p>Câu 1: ...</p>",
  });
}

app.listen(3000, () => console.log("Server đang chạy trên cổng 3000"));
