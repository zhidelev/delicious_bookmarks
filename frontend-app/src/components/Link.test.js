import { render, screen } from '@testing-library/react';
import Link from './Link';

test('renders learn react link', () => {
  render(<Link />);
  const linkElement = screen.getByText(/Link/i);
  expect(linkElement).toBeInTheDocument();
});
