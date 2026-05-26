import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { App } from "../../starter/src/App";

test("approval persists when switching employee filters", async () => {
  const user = userEvent.setup();
  render(<App />);

  const aliceTx = screen.getByLabelText("approve-t1") as HTMLInputElement;
  expect(aliceTx.checked).toBe(false);
  await user.click(aliceTx);
  expect(aliceTx.checked).toBe(true);

  const filter = screen.getByLabelText("Employee");
  await user.selectOptions(filter, "Bob");
  await user.selectOptions(filter, "Alice");

  const aliceTxAfter = screen.getByLabelText("approve-t1") as HTMLInputElement;
  expect(aliceTxAfter.checked).toBe(true);
});

test("toggling one employee does not mutate unrelated employees", async () => {
  const user = userEvent.setup();
  render(<App />);

  const bobTx = screen.getByLabelText("approve-t3") as HTMLInputElement;
  expect(bobTx.checked).toBe(true);

  const aliceTx = screen.getByLabelText("approve-t2") as HTMLInputElement;
  await user.click(aliceTx);
  expect(aliceTx.checked).toBe(true);

  const filter = screen.getByLabelText("Employee");
  await user.selectOptions(filter, "Bob");

  const bobTxAfter = screen.getByLabelText("approve-t3") as HTMLInputElement;
  expect(bobTxAfter.checked).toBe(true);
});
