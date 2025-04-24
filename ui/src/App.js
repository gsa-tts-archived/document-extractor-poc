import { BrowserRouter, Routes, Route } from 'react-router';
import UploadPage from './pages/UploadPage';
import VerifyPage from './pages/VerifyPage';
import DownloadPage from './pages/DownloadPage';
import SignInPage from './pages/SignInPage';
import { useEffect, useState } from 'react';

export default function App() {
  const [authToken, setAuthToken] = useState(() => {
    return sessionStorage.getItem('auth_token') || '';
  });

  useEffect(() => {
    sessionStorage.setItem('auth_token', authToken);
  }, [authToken]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/verify-document" element={<VerifyPage />} />
        <Route path="/download-document" element={<DownloadPage />} />
        <Route path="/upload-document" element={<UploadPage />} />
        <Route path="/" element={<SignInPage setAuthToken={setAuthToken} />} />
      </Routes>
    </BrowserRouter>
  );
}
