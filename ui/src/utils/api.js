export async function authorizedFetch(url, options = {}) {
  const token = sessionStorage.getItem('auth_token');

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  const fetchOptions = {
    ...options,
    headers,
  };

  const res = await fetch(url, fetchOptions);

  return res;
}

export async function logout() {
  sessionStorage.removeItem('auth_token');
  window.location.href = '/';
}
