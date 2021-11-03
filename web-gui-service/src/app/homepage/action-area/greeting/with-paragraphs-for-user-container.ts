import { addToStringArrayIfNotPresent, removeFromStringArray } from "src/app/utils";


function hideParagraphsForUserContainer(obj: WithParagraphsForUserContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.paragraphsForUserContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.paragraphsForUserContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  );
}

function initialClassesForParagraphsForUserContainer(): Array<string> {
  let result = [
    "animated",
    "debug",
    "whitespaced-completely"
  ]
  return result
}

function showParagraphsForUserContainer(obj: WithParagraphsForUserContainer): void {
  removeFromStringArray(obj.paragraphsForUserContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.paragraphsForUserContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.paragraphsForUserContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.paragraphsForUserContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  );
}

interface WithParagraphsForUserContainer {
  animationTimeout: number,
  paragraphsForUserContainerClasses: Array<string>
}

export {
  hideParagraphsForUserContainer,
  initialClassesForParagraphsForUserContainer,
  showParagraphsForUserContainer,
  WithParagraphsForUserContainer
}
