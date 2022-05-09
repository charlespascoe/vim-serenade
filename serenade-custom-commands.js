// This file includes various examples of how to navigate and control Vim with
// custom Serenade voice commands.

const vim = serenade.app('Vim');

vim.command(
  'split',
  (api) => api.evaluateInPlugin('vsplit'),
);

vim.command(
  'horizontal split',
  (api) => api.evaluateInPlugin('split'),
);

vim.command(
  'back',
  (api) => api.evaluateInPlugin('exec "normal \\<C-o>"'),
);

vim.command(
  'forward',
  // Not sure why "exec normal" doesn't work
  (api) => api.evaluateInPlugin('call feedkeys("\\<Esc>\\<C-i>")'),
);

vim.command(
  'window left',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>h"'),
);

vim.command(
  'window down',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>j"'),
);

vim.command(
  'window up',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>k"'),
);

vim.command(
  'window right',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>l"'),
);

vim.command(
  'swap window left',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>H"'),
);

vim.command(
  'swap window down',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>J"'),
);

vim.command(
  'swap window up',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>K"'),
);

vim.command(
  'swap window right',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>L"'),
);

vim.command(
  'window zoom',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>z"'),
);

vim.command(
  'normalise windows',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>="'),
);

vim.command(
  'switch',
  (api) => api.evaluateInPlugin('exec "normal \\<C-w>\\<C-w>"'),
);

vim.command(
  'top',
  (api) => api.evaluateInPlugin('normal zt'),
);

vim.command(
  'center',
  (api) => api.evaluateInPlugin('normal zz'),
);

vim.command(
  'bottom',
  (api) => api.evaluateInPlugin('normal zb'),
);

vim.command(
  'high',
  (api) => api.evaluateInPlugin('normal H'),
);

vim.command(
  'middle',
  (api) => api.evaluateInPlugin('normal M'),
);

vim.command(
  'low',
  (api) => api.evaluateInPlugin('normal L'),
);

vim.command(
  'turn on spelling',
  (api) => api.evaluateInPlugin('set spell'),
);

vim.command(
  'turn off spelling',
  (api) => api.evaluateInPlugin('set nospell'),
);

vim.command(
  'close',
  (api) => api.evaluateInPlugin('q'),
  {autoExecute: false},
);

vim.command(
  'close file',
  (api) => api.evaluateInPlugin('bdelete'),
  {autoExecute: false},
);
