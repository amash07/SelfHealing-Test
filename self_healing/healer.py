from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class SelfHealing:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):

        # =====================================
        # TRY ORIGINAL LOCATOR
        # =====================================

        try:

            element = self.driver.find_element(
                by,
                value
            )

            return element

        except Exception:

            print()
            print("----------------------------------------")
            print("SELF-HEALING ACTIVATED")
            print("----------------------------------------")

            print(
                f"Original locator failed:"
            )

            print(
                f"    {by} = {value}"
            )


        # =====================================
        # READ PAGE DOM
        # =====================================

        soup = BeautifulSoup(
            self.driver.page_source,
            "html.parser"
        )


        candidates = []


        # =====================================
        # SEARCH ELEMENTS
        # =====================================

        for element in soup.find_all(
            ["button", "a", "input"]
        ):

            element_id = element.get("id")

            element_name = element.get("name")

            text = element.get_text(
                strip=True
            )


            score = 0

            reasons = []


            # =================================
            # ID SIMILARITY
            # =================================

            if element_id:

                original = value.lower()

                candidate = element_id.lower()


                # loginButton -> loginBtn
                # profileLink -> profileBtn
                # settingsLink -> settingsBtn

                original_clean = (
                    original
                    .replace("button", "")
                    .replace("link", "")
                    .replace("btn", "")
                )

                candidate_clean = (
                    candidate
                    .replace("button", "")
                    .replace("link", "")
                    .replace("btn", "")
                )


                if original_clean == candidate_clean:

                    score += 60

                    reasons.append(
                        "similar ID pattern"
                    )


            # =================================
            # TEXT MATCHING
            # =================================

            if text:

                text_lower = text.lower()

                value_lower = value.lower()


                if (
                    "login" in value_lower
                    and "login" in text_lower
                ):

                    score += 40

                    reasons.append(
                        "matching Login text"
                    )


                elif (
                    "profile" in value_lower
                    and "profile" in text_lower
                ):

                    score += 40

                    reasons.append(
                        "matching Profile text"
                    )


                elif (
                    "settings" in value_lower
                    and "settings" in text_lower
                ):

                    score += 40

                    reasons.append(
                        "matching Settings text"
                    )


            # =================================
            # SAVE CANDIDATE
            # =================================

            if score > 0:

                candidates.append(
                    {
                        "element": element,
                        "id": element_id,
                        "name": element_name,
                        "text": text,
                        "score": score,
                        "reasons": reasons
                    }
                )


        # =====================================
        # NO CANDIDATE
        # =====================================

        if not candidates:

            raise Exception(
                "Self-healing failed. "
                "No replacement element found."
            )


        # =====================================
        # BEST CANDIDATE
        # =====================================

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        best = candidates[0]


        print()
        print("Replacement candidate found:")

        print(
            f"    Tag: "
            f"{best['element'].name}"
        )

        print(
            f"    ID: "
            f"{best['id']}"
        )

        print(
            f"    Text: "
            f"{best['text']}"
        )

        print(
            f"    Score: "
            f"{best['score']}"
        )


        print()

        for reason in best["reasons"]:

            print(
                f"    Reason: {reason}"
            )


        # =====================================
        # USE RECOVERED ID
        # =====================================

        if best["id"]:

            healed_element = self.driver.find_element(
                By.ID,
                best["id"]
            )

            print()

            print(
                "[SELF-HEALING] "
                "✓ Locator recovered"
            )

            print(
                f"    Original: {value}"
            )

            print(
                f"    Recovered: {best['id']}"
            )

            return healed_element


        raise Exception(
            "Candidate found but no usable locator."
        )