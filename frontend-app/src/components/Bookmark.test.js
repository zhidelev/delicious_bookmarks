import { render, screen } from '@testing-library/react';
import Bookmark from './Bookmark.js';

test('renders learn react link', () => {
  render(<Bookmark />);
  const linkElement = screen.getByText(/Title/i);
  expect(linkElement).toBeInTheDocument();
});
