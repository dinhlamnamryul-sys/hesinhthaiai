import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Mock data
const data = {
  "Lớp 6": {
    "Chương 2: Số nguyên": {
      "Cộng trừ số nguyên": [
        { question: "Tính: -3 + (-11)", answer: -14, hintVN: "Cộng hai số nguyên âm: Cộng hai giá trị tuyệt đối rồi đặt dấu trừ.", hintHM: "Ntxiv ob qho kev sib npaug tsis zoo: ntxiv ob qho ob cho tseem ceeb thiab tom qab muab cov paib rho tawm hauv ntej." }
      ]
    }
  }
};

export default function App() {
  const [grade, setGrade] = useState("");
  const [chapter, setChapter] = useState("");
  const [lesson, setLesson] = useState("");
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [currentQ, setCurrentQ] = useState(null);

  const grades = Object.keys(data);
  const chapters = grade ? Object.keys(data[grade]) : [];
  const lessons = chapter ? Object.keys(data[grade][chapter]) : [];

  const loadQuestion = () => {
    const q = data[grade][chapter][lesson][0];
    setCurrentQ(q);
    setResult(null);
    setInput("");
  };

  const check = () => {
    if (!currentQ) return;
    setResult(Number(input) === currentQ.answer);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card className="p-4 col-span-1">
        <h2 className="font-bold text-lg mb-4">Chọn Bài Học</h2>
        <select className="w-full p-2 border rounded mb-3" value={grade} onChange={e => {setGrade(e.target.value); setChapter(""); setLesson("");}}>
          <option value="">-- Chọn lớp --</option>
          {grades.map(g => <option key={g}>{g}</option>)}
        </select>
        {grade && (
          <select className="w-full p-2 border rounded mb-3" value={chapter} onChange={e => {setChapter(e.target.value); setLesson("");}}>
            <option value="">-- Chọn chương --</option>
            {chapters.map(c => <option key={c}>{c}</option>)}
          </select>
        )}
        {chapter && (
          <select className="w-full p-2 border rounded mb-3" value={lesson} onChange={e => setLesson(e.target.value)}>
            <option value="">-- Chọn bài --</option>
            {lessons.map(l => <option key={l}>{l}</option>)}
          </select>
        )}
        <Button className="w-full" onClick={loadQuestion} disabled={!lesson}>Đặt bài</Button>
      </Card>

      <Card className="p-4 col-span-2">
        {!currentQ ? (
          <p>Hãy chọn bài để bắt đầu.</p>
        ) : (
          <CardContent>
            <h2 className="font-bold text-xl mb-4">Câu hỏi:</h2>
            <p className="text-2xl mb-4">{currentQ.question}</p>

            <input className="border p-2 rounded w-40 text-center" value={input} onChange={e => setInput(e.target.value)} />
            <Button className="ml-3" onClick={check}>Kiểm tra</Button>

            {result !== null && (
              <div className="mt-4 p-3 rounded text-white" style={{background: result ? "green" : "red"}}>
                {result ? "Đúng rồi!" : `Sai rồi! Đáp án đúng: ${currentQ.answer}`}
              </div>
            )}

            {result === false && (
              <div className="mt-4 space-y-2">
                <div className="p-3 bg-green-100 rounded">💡 Gợi ý (Tiếng Việt): {currentQ.hintVN}</div>
                <div className="p-3 bg-red-100 rounded">🧠 H'Mông: {currentQ.hintHM}</div>
              </div>
            )}
          </CardContent>
        )}
      </Card>
    </div>
  );
}
