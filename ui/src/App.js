import { Routes, Route, useNavigate } from 'react-router';
import UploadPage from './pages/UploadPage';
import VerifyPage from './pages/VerifyPage';
import DownloadPage from './pages/DownloadPage';
import SignInPage from './pages/SignInPage';
import { useEffect, useState } from 'react';

export default function App() {
  const [authToken, setAuthToken] = useState(() => {
    return sessionStorage.getItem('auth_token') || '';
  });

  const [justSignedOut, setJustSignedOut] = useState(false);

  const navigate = useNavigate();

  async function signOut() {
    setAuthToken('');
    setJustSignedOut(true);
    navigate('/');
  }

  useEffect(() => {
    if (authToken) {
      sessionStorage.setItem('auth_token', authToken);
      setJustSignedOut(false);
    } else {
      sessionStorage.removeItem('auth_token');
    }
  }, [authToken]);

  return (
    <Routes>
      <Route path="/verify-document" element={<VerifyPage />} />
      <Route path="/download-document" element={<DownloadPage />} />
      <Route
        path="/upload-document"
        element={<UploadPage signOut={signOut} />}
      />
      <Route
        path="/"
        element={
          <SignInPage
            setAuthToken={setAuthToken}
            justSignedOut={justSignedOut}
          />
        }
      />
    </Routes>
  );
}
