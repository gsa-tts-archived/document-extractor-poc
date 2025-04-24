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

  return await fetch(url, fetchOptions);
}
