import { addToStringArrayIfNotPresent, removeFromStringArray } from "src/app/utils";

function hideParagraphsForGuestContainer(obj: WithParagraphsForGuestContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.paragraphsForGuestContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.paragraphsForGuestContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  );
}

function initialClassesForParagraphsForGuestContainer(): Array<string> {
  let result = [
    "animated",
    "debug",
    "whitespaced-completely"
  ]
  return result;
}

function showParagraphsForGuestContainer(obj: WithParagraphsForGuestContainer): void {
  removeFromStringArray(obj.paragraphsForGuestContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.paragraphsForGuestContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.paragraphsForGuestContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.paragraphsForGuestContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  )
}

interface WithParagraphsForGuestContainer {
  animationTimeout: number;
  paragraphsForGuestContainerClasses: Array<string>
}

export {
  hideParagraphsForGuestContainer,
  initialClassesForParagraphsForGuestContainer,
  showParagraphsForGuestContainer,
  WithParagraphsForGuestContainer
}
