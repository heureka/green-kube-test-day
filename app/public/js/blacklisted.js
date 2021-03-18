/**
 * Redirect human detected as a robot to password withdrawal site without blacklist.
 */
function RedirectWithoutBlacklist(res) {
  window.location.href = window.location.pathname + '?skip-blacklist' + window.location.hash
}