import * as d3 from "d3";

const classSize = 10;

class IdCounts {
    constructor() {
        this.counts = {}
    }
    increment(id) {
        if (this.counts[id] === undefined) {
            this.counts[id] = 1;
        } else {
            this.counts[id] += 1;
        }
    }
    decrement(id) {
        if (this.counts[id] !== undefined) {
            this.counts[id] -= 1;
        }
    }
}

class ChoiceResponseDataView {
    constructor(responseList) {
        this.responseMap = this.#buildResponseMap(responseList);
        this.#buildSummary()
    }

    #buildResponseMap(responseList) {
        const responseMap = {};
        responseList.forEach((response) => {
            responseMap[response.user_id] = response
        });
        return responseMap
    }

    #buildSummary() {
        this.selectedOptionCounts = new IdCounts();
        Object.values(this.responseMap).forEach((response) => {
            this.#addResponseToSummary(response);
        });
    }

    #addResponseToSummary(response) {
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.increment(selectedId));
    }

    #removeUserResponseFromSummary(userId) {
        const response = this.responseMap[userId];
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.decrement(selectedId));
    }

    renderSummary() {
        for (const [optionId, answeredCount] of Object.entries(this.selectedOptionCounts.counts)) {
            this.#renderChoiceOptionSummary(optionId, answeredCount);
        }
    }

    updateResponse(response) {
        if (this.responseMap[response.user_id] !== undefined) {
            this.#removeUserResponseFromSummary(response.user_id);
        }
        this.responseMap[response.user_id] = response;
        this.#addResponseToSummary(response);
        this.renderSummary();
    }

    #renderChoiceOptionSummary(optionId, answered_count) {
        var myScale = d3.scaleLinear()
            .domain([0, classSize])
            .range([0, 100]);
        d3.selectAll(`.question-choice[option-id="${optionId}"] .response-chart`)
          .selectAll('rect')
          .data([answered_count])
          .join('rect')
            .transition()
          .attr('width', function(d) {
            return `${myScale(d)}%`;
          });
    }
}

const questionResponseTrackers = {};

export default {
    initializeDisplays(response_map) {
        for (const [questionId, responseList] of Object.entries(response_map)) {
            const $questionElement = $(`.apella-question[questionId="${questionId}"]`);
            if ($questionElement.hasClass('choice')) {
                let tracker = new ChoiceResponseDataView(responseList);
                tracker.renderSummary();
                questionResponseTrackers[questionId] = tracker;
            }
        }
    },
    updateResponse(questionId, response) {
        questionResponseTrackers[questionId].updateResponse(response);
    }
}
