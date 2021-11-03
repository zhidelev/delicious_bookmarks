import { render, screen } from '@testing-library/react';
import App from './App';

test('app has header part', () => {
  render(<App />);
  const header = screen.getByText(/Header/i);
  expect(header).toBeInTheDocument();
});

test('app has footer part', () => {
  render(<App />);
  const footer = screen.getByText(/Footer/i);
  expect(footer).toBeInTheDocument();
});
