var table = document.querySelector("#brandBand_2 > div > div > div > div > div.searchScrollerWrapper > div > div > div.forcesearch-results-grid-lvm-desktop.slds-table_joined.test-listViewManager.slds-card.slds-card_boundary.slds-grid.slds-grid--vertical.forceListViewManager.forceSearchResultsGridLVM > div > div > div > div.col-0-wrap.col-1-wrap.col-2-wrap.col-3-wrap.col-4-wrap.hideRowNumberColumn.hideSelection.forceListViewManagerGrid > div.listViewContent.slds-table--header-fixed_container > div.uiScroller.scroller-wrapper.scroll-bidirectional.native > div > div > table > tbody");


function Scroll() {

    var lastRow = table.rows[ table.rows.length - 1 ];
    lastRow.scrollIntoView();

    setTimeout(Scroll, 1000);
}

Scroll();
