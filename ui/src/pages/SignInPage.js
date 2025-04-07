import { useState } from 'react';

import Layout from '../components/Layout';

export default function SignInPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  function handleLogin(e) {
    e.preventDefault();
    if (!username || !password) {
      setError('Please enter both username and password.');
      return;
    }
    console.log('logging in with:', { username, password });
  }

  return (
    <Layout>
      <div
        className="grid-row flex-column minh-viewport bg-primary-lighter"
        style={{ minHeight: 'calc(100vh - 222px)' }}
      >
        <div className="bg-white margin-top-10 radius-md padding-y-4 card margin-x-auto maxw-tablet tablet:padding-y-8 padding-x-2 tablet:padding-x-10 tablet:margin-bottom-8">
          <h1>Sign in for existing users</h1>
          <form onSubmit={handleLogin}>
            <div>
              <label className="usa-label" htmlFor="input-type-text">
                Username
              </label>
              <input
                className="usa-input"
                id="username"
                placeholder="username"
                name="username"
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <label className="usa-label" htmlFor="input-type-text">
                Password
              </label>
              <input
                className="usa-input"
                id="password"
                placeholder="password"
                name="password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button type="submit" className="usa-button">
              Sign in
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}
