function shouldUseTextarea(value) {
  if (typeof value !== 'string') return false;
  return value.includes('\n');
}

module.exports = { shouldUseTextarea };
