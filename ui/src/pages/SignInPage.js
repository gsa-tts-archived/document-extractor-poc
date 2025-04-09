import { useState } from 'react';

import Layout from '../components/Layout';

async function mockLogin(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === 'admin' && password === 'password123') {
        resolve({ token: 'mock-jwt-token' });
      } else {
        reject(new Error('The email or password you’ve entered is wrong.'));
      }
    }, 500);
  });
}

export default function SignInPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [formError, setFormError] = useState('');

  async function handleLogin(e) {
    e.preventDefault();
    // Clear previous error messages:
    setUsernameError('');
    setPasswordError('');
    setFormError('');

    let hasError = false;

    if (!username) {
      setUsernameError('Please enter your username');
      hasError = true;
    }

    if (!password) {
      setPasswordError('Please enter your password');
      hasError = true;
    }

    if (hasError) return;

    try {
      const response = await mockLogin(username, password);
      console.log('Logged in! Token:', response.token);
      sessionStorage.setItem('token', response.token);
      // redirect to login page
    } catch (err) {
      setFormError(err.message);
    }
  }

  return (
    <Layout>
      <div className="site-wrapper bg-primary-lighter grid-row flex-column minh-viewport flex-align-center flex-justify-center">
        <div className="bg-white margin-top-10 radius-md padding-y-4 card margin-x-auto width-tablet tablet:padding-y-8 padding-x-2 tablet:padding-x-10 tablet:margin-bottom-8">
          {formError && (
            <div className="usa-alert usa-alert--error">
              <div className="usa-alert__body">
                <p className="usa-alert__text">{formError}</p>
              </div>
            </div>
          )}

          <div className="usa-alert usa-alert--info">
            <div className="usa-alert__body">
              <p className="usa-alert__text">Signed out successfully.</p>
            </div>
          </div>
          <h1>Sign in for existing users</h1>

          <form onSubmit={handleLogin} id="signin-form">
            <div className="usa-form-group usa">
              <label className="usa-label" htmlFor="username">
                Username
              </label>
              {usernameError && (
                <span className="usa-error-message" role="alert">
                  {usernameError}
                </span>
              )}
              <input
                className="usa-input usa-input--big"
                id="username"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            <div className="usa-form-group">
              <label className="usa-label" htmlFor="input-type-text">
                Password
              </label>
              {passwordError && (
                <span className="usa-error-message" role="alert">
                  {passwordError}
                </span>
              )}
              <input
                className="usa-input margin-bottom-2 usa-input--big"
                id="password"
                name="password"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="usa-button usa-button--big width-full"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}
