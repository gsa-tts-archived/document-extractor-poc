import { BrowserRouter, Routes, Route } from 'react-router';
import UploadPage from './pages/UploadPage';
import VerifyPage from './pages/VerifyPage';
import DownloadPage from './pages/DownloadPage';
import SignInPage from './pages/SignInPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/verify-document" element={<VerifyPage />} />
        <Route path="/download-document" element={<DownloadPage />} />
        <Route path="/upload-document" element={<UploadPage />} />
        <Route path="/" element={<SignInPage />} />
      </Routes>
    </BrowserRouter>
  );
}
