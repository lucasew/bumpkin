{ fetchurl }:
{ declared, fetched }:
fetchurl {
  name = "source.${fetched.file_type}";
  url = fetched.final_url;
  sha256 = fetched.sha256;
}
