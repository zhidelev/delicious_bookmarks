import { render, screen } from '@testing-library/react';
import AppFooter from './AppFooter';

test('renders App Footer', () => {
  render(<AppFooter />);
  const footer = screen.getByText(/Footer/i);
  expect(footer).toBeInTheDocument();
});