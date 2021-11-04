import { addToStringArrayIfNotPresent, removeFromStringArray } from "src/app/utils";

function initialRequestErrorContainerClasses(): Array<string> {
  return [
    "animated",
    "debug",
    "whitespaced-completely"
  ]
}

function hideRequestErrorContainer(obj: WithRequestErrorContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.requestErrorContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.requestErrorContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  );
}

function showRequestErrorContainer(obj: WithRequestErrorContainer): void {
  removeFromStringArray(obj.requestErrorContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.requestErrorContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.requestErrorContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.requestErrorContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  );
}

interface WithRequestErrorContainer {
  animationTimeout: number;
  requestErrorContainerClasses: Array<string>;
}

export {
  hideRequestErrorContainer,
  initialRequestErrorContainerClasses,
  showRequestErrorContainer,
  WithRequestErrorContainer
}
