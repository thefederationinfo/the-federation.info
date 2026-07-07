const websiteID =
  document.getElementById("trker").attributes["data-website-id"].value;

const track = (path) => {
  try {
    window.umami.track({
      website: websiteID,
      url: path || document.location.pathname,
      title: document.title,
      referrer: document.referrer,
    });
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn("could not find umami, ignoring telemetry");
  }
};

const trackEvent = (name) => {
  try {
    window.umami.track(name);
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn("could not find umami, ignoring telemetry");
  }
};

export default track;
export { trackEvent };
