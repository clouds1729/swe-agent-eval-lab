import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { App } from "../../starter/src/App";

test("toggles approval in current view", async () => {
  const user = userEvent.setup();
  render(<App />);

  const checkbox = screen.getByLabelText("approve-t1") as HTMLInputElement;
  expect(checkbox.checked).toBe(false);

  await user.click(checkbox);
  expect(checkbox.checked).toBe(true);
});
