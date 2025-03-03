import React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import UploadPage from "./pages/UploadPage";
import VerifyPage from "./pages/VerifyPage";
import DownloadPage from "./pages/DownloadPage";

export default function App() {
    return (
        <BrowserRouter>
        <Routes>
          <Route path="/verify-document" element={<VerifyPage />} />
          <Route path="/download-document" element={<DownloadPage />} />
          <Route path="/" element={<UploadPage />} />
        </Routes>
        </BrowserRouter>
    )
}
