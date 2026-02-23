/**
 * Generic autocomplete autofill for Django admin.
 *
 * Reads `data-autofill` JSON from any autocomplete <select> and fills
 * target fields in the same inline row when a selection is made.
 *
 * Configuration (on the source <select> widget via AutofillInlineMixin):
 *   data-autofill='{"price_q": "base_price_q"}'
 *
 * This means: on change, read data[0].base_price_q from Select2 cache
 * and fill the input whose name ends with "-price_q" in the same row.
 *
 * Requires: the backend serialize_result must include the source keys
 * in the autocomplete JSON response.
 */
(function() {
    "use strict";

    function init() {
        var $ = django.jQuery;

        // Delegated change handler — works regardless of Select2 init timing
        $(document).on("change", "select[data-autofill]", function() {
            var select = this;
            var $select = $(select);
            var mapping;

            try {
                mapping = JSON.parse(select.dataset.autofill);
            } catch (e) {
                return;
            }

            var data = $select.select2("data");
            if (!data || !data[0]) return;

            var row = select.closest(".form-row") || select.closest("tr");
            if (!row) return;

            var selected = data[0];

            Object.keys(mapping).forEach(function(targetSuffix) {
                var sourceKey = mapping[targetSuffix];
                var target = row.querySelector('input[name$="-' + targetSuffix + '"]');
                if (!target) return;

                var value = selected[sourceKey];
                if (value === undefined || value === null) return;

                // Readonly fields: always fill (user can't edit)
                // Editable fields: skip if user manually entered a value
                if (!target.readOnly && target.value && target.dataset.autoFilled !== "true") return;

                target.value = value;
                target.dataset.autoFilled = "true";
            });
        });

        // Track manual edits — clear auto-filled flag
        $(document).on("input", "input[data-auto-filled]", function() {
            this.dataset.autoFilled = "false";
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
