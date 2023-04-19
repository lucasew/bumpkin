{ fetchurl }:
{ declared, fetched }:
fetchurl {
  url = fetched.final_url;
  sha256 = fetched.sha256;
  allowSubstitutes = false;
}
