import { render, screen } from '@testing-library/react';
import AppHeader from './AppHeader';

test('renders App Header', () => {
  render(<AppHeader />);
  const header = screen.getByText(/Header/i);
  expect(header).toBeInTheDocument();
});
