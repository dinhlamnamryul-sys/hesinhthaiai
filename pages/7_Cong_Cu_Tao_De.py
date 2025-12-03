// Single-file React component (usable in a Create React App / Vite / Next.js page)
// Frontend: uploads 3 files (sách giáo khoa, công văn, mẫu đề), nhận câu lệnh người dùng,
// gửi lên backend; backend trả về JSON chứa `matrixHtml` và `examHtml` (HTML strings)
// Frontend sẽ hiển thị bản xem trước, cho phép tải về dưới dạng .docx (simple blob) hoặc sao chép.

import React, { useState } from 'react';

export default function ExamGenerator() {
  const [textbookFile, setTextbookFile] = useState(null);
  const [docFile, setDocFile] = useState(null);
  const [templateFile, setTemplateFile] = useState(null);
  const [instruction, setInstruction] = useState('Tạo ma trận và đề kiểm tra theo mẫu');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState({ matrixHtml: '', examHtml: '' });
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (!textbookFile || !docFile || !templateFile) {
      setError('Vui lòng tải lên cả 3 file: sách giáo khoa, công văn, và mẫu đề.');
      return;
    }

    const fd = new FormData();
    fd.append('textbook', textbookFile);
    fd.append('document', docFile);
    fd.append('template', templateFile);
    fd.append('instruction', instruction);

    setLoading(true);
    try {
      const res = await fetch('/api/generate', { method: 'POST', body: fd });
      if (!res.ok) throw new Error(await res.text());
      const json = await res.json();
      setResult({ matrixHtml: json.matrixHtml, examHtml: json.examHtml });
    } catch (err) {
      console.error(err);
      setError('Có lỗi khi gọi API: ' + (err.message || err));
    } finally {
      setLoading(false);
    }
  }

  function downloadHtmlAsDocx(html, filename) {
    const preface = "<html><head><meta charset=\"utf-8\"></head><body>";
    const blob = new Blob([preface + html + '</body></html>'], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-2xl shadow">
        <h1 className="text-2xl font-semibold mb-4">Trình tạo Ma trận & Đề kiểm tra (AI)</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Sách giáo khoa (PDF/DOCX)</label>
            <input type="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" onChange={e => setTextbookFile(e.target.files[0])} />
            {textbookFile && <div className="text-xs text-gray-600 mt-1">{textbookFile.name}</div>}
          </div>
          <div>
            <label className="block text-sm font-medium">Công văn / Công bố (PDF/DOCX)</label>
            <input type="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" onChange={e => setDocFile(e.target.files[0])} />
            {docFile && <div className="text-xs text-gray-600 mt-1">{docFile.name}</div>}
          </div>
          <div>
            <label className="block text-sm font-medium">Mẫu đề kiểm tra (Word/PDF) — định dạng mong muốn</label>
            <input type="file" accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" onChange={e => setTemplateFile(e.target.files[0])} />
            {templateFile && <div className="text-xs text-gray-600 mt-1">{templateFile.name}</div>}
          </div>

          <div>
            <label className="block text-sm font-medium">Câu lệnh / Yêu cầu với AI</label>
            <textarea value={instruction} onChange={e => setInstruction(e.target.value)} rows={3} className="w-full p-2 border rounded" />
          </div>

          {error && <div className="text-red-600">{error}</div>}

          <div className="flex gap-3">
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded" disabled={loading}>{loading ? 'Đang xử lý...' : 'Tạo ma trận & đề'}</button>
            <button type="button" className="px-4 py-2 border rounded" onClick={() => { setResult({ matrixHtml: '', examHtml: '' }); setError(''); }}>Xóa kết quả</button>
          </div>
        </form>

        <div className="mt-6">
          <h2 className="text-lg font-medium">Kết quả</h2>

          {result.matrixHtml ? (
            <div className="mt-4">
              <h3 className="font-semibold">Ma trận (xem trước)</h3>
              <div className="mt-2 p-4 border rounded bg-white" dangerouslySetInnerHTML={{ __html: result.matrixHtml }} />
              <div className="mt-2 flex gap-2">
                <button className="px-3 py-1 border rounded" onClick={() => downloadHtmlAsDocx(result.matrixHtml, 'matran.docx')}>Tải ma trận (.docx)</button>
                <button className="px-3 py-1 border rounded" onClick={() => navigator.clipboard.writeText(result.matrixHtml)}>Sao chép HTML</button>
              </div>
            </div>
          ) : <div className="text-sm text-gray-500 mt-2">Chưa có ma trận</div>}

          {result.examHtml ? (
            <div className="mt-4">
              <h3 className="font-semibold">Đề kiểm tra (xem trước)</h3>
              <div className="mt-2 p-4 border rounded bg-white" dangerouslySetInnerHTML={{ __html: result.examHtml }} />
              <div className="mt-2 flex gap-2">
                <button className="px-3 py-1 border rounded" onClick={() => downloadHtmlAsDocx(result.examHtml, 'dekiemtra.docx')}>Tải đề (.docx)</button>
                <button className="px-3 py-1 border rounded" onClick={() => navigator.clipboard.writeText(result.examHtml)}>Sao chép HTML</button>
              </div>
            </div>
          ) : <div className="text-sm text-gray-500 mt-2">Chưa có đề</div>}
        </div>

        <div className="mt-6 text-xs text-gray-500">
          <strong>Ghi chú:</strong> Frontend này chỉ gửi file và câu lệnh tới backend. Backend chịu trách nhiệm:
          <ol className="list-decimal ml-6">
            <li>Trích xuất nội dung từ PDF/DOCX (ví dụ dùng pdf-parse, mammoth).</li>
            <li>Gửi nội dung và mẫu đến mô hình AI (OpenAI / local LLM) để yêu cầu tạo ma trận và đề theo đúng mẫu.</li>
            <li>Trả về HTML đã format sẵn (matrixHtml và examHtml) để frontend hiển thị / tải về.</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

/*
----------------------
Sample backend (Node.js + Express) — lưu ở server.js (ví dụ). Đây là ví dụ minh hoạ, bạn cần cài thêm các package:
npm i express multer axios form-data pdf-parse mammoth dotenv

Mã backend ví dụ (không đưa API key ở đây):

const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');
const axios = require('axios');
require('dotenv').config();

const upload = multer({ dest: 'uploads/' });
const app = express();

function readFileText(filePath, mimetype) {
  if (mimetype === 'application/pdf') {
    const data = fs.readFileSync(filePath);
    return pdfParse(data).then(r => r.text);
  } else if (mimetype.includes('word')) {
    return mammoth.extractRawText({ path: filePath }).then(r => r.value);
  } else {
    return Promise.resolve(fs.readFileSync(filePath, 'utf8'));
  }
}

app.post('/api/generate', upload.fields([{ name: 'textbook' }, { name: 'document' }, { name: 'template' }]), async (req, res) => {
  try {
    const instruction = req.body.instruction || '';
    const files = req.files;
    // read files
    const tb = await readFileText(files['textbook'][0].path, files['textbook'][0].mimetype);
    const cv = await readFileText(files['document'][0].path, files['document'][0].mimetype);
    const template = await readFileText(files['template'][0].path, files['template'][0].mimetype);

    // build prompt for AI
    const prompt = `You are an assistant that must produce TWO HTML outputs: a matrix table (label: <<MATRIX>>) and an exam (label: <<EXAM>>).\n\n` +
      `Textbook content:\n${tb}\n\nOfficial doc:\n${cv}\n\nTemplate (shows desired layout):\n${template}\n\nUser instruction:\n${instruction}\n\nIMPORTANT: Return ONLY JSON with keys matrixHtml and examHtml, each containing valid HTML fragments representing the matrix and the exam respectively.`;

    // Call OpenAI (pseudo). Replace with your call to OpenAI ChatCompletions or Responses API.
    // Example using axios to call your own server that proxies to OpenAI or the OpenAI SDK.

    // For simplicity here we'll call a fake function `callOpenAI(prompt)` that should return the text.

    const aiResponseText = await callOpenAI(prompt);

    // Expect aiResponseText to be JSON parseable
    let parsed;
    try {
      parsed = JSON.parse(aiResponseText);
    } catch (e) {
      // If model returned plain text with markers, you may need to parse by markers <<MATRIX>> and <<EXAM>>
      const m1 = aiResponseText.indexOf('<<MATRIX>>');
      const m2 = aiResponseText.indexOf('<<EXAM>>');
      if (m1 >= 0 && m2 >= 0) {
        const matrixHtml = aiResponseText.substring(m1 + '<<MATRIX>>'.length, m2).trim();
        const examHtml = aiResponseText.substring(m2 + '<<EXAM>>'.length).trim();
        parsed = { matrixHtml, examHtml };
      } else {
        throw new Error('AI trả về kết quả không rõ định dạng');
      }
    }

    // cleanup uploaded files
    Object.values(files).flat().forEach(f => fs.unlinkSync(f.path));

    res.json({ matrixHtml: parsed.matrixHtml, examHtml: parsed.examHtml });
  } catch (err) {
    console.error(err);
    res.status(500).send(String(err));
  }
});

async function callOpenAI(prompt) {
  // Implement this function to call OpenAI's API (or another LLM). Here's a sketch using the OpenAI REST API.
  // Make sure to keep your API key secret on the server side.

  // Example using axios + OpenAI (pseudo):
  // const r = await axios.post('https://api.openai.com/v1/chat/completions', { model: 'gpt-4o-mini', messages: [{ role: 'user', content: prompt }], max_tokens: 3000 }, { headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } });
  // return r.data.choices[0].message.content;

  // For safety here, return a small example JSON:
  return JSON.stringify({ matrixHtml: '<table><tr><th>Chủ đề</th><th>Số câu</th></tr><tr><td>Phép nhân</td><td>4</td></tr></table>', examHtml: '<h1>Đề kiểm tra mẫu</h1><p>1. Viết...</p>' });
}

app.listen(3000, () => console.log('Server listening on 3000'));

----------------------
Hướng dẫn triển khai ngắn gọn:
1) Frontend: thêm component React trên vào dự án (CRA/Vite/Next). Cài Tailwind nếu muốn giao diện giống ví dụ.
2) Backend: cài Node/Express theo phần ví dụ, set biến môi trường OPENAI_API_KEY.
3) Tinh chỉnh `callOpenAI` để gọi OpenAI hoặc LLM bạn dùng. Nên hạn chế đưa toàn bộ sách giáo khoa trong 1 prompt nếu quá dài: thực hiện tóm tắt / trích xuất trước khi gọi LLM hoặc dùng vector DB.
4) Thiết kế prompt rõ ràng: yêu cầu output ở dạng JSON với 2 trường `matrixHtml` và `examHtml` để frontend dễ parse.

Bảo mật & Lưu ý:
- Không đưa API key ra client.
- Nếu file lớn (PDF sách), xử lý server-side: OCR (tesseract) nếu PDF là ảnh.
- Kiểm thử kỹ các mẫu đề để tránh lỗi định dạng.
*/
