import React from 'react';
import { ArrowRight } from '@gravity-ui/icons';

import './BreadCrumbs.css'

export interface PagesNamesWithLinks {
    pageName: string;
    pageUrl: string;
}

interface BreadCrumbsProps {
    currentPageName: string;
    pagesBehind: Array<PagesNamesWithLinks>
}

export default function BreadCrumbs({ currentPageName, pagesBehind }: BreadCrumbsProps) {
    return (
        <div className="bread-crumbs">
            {pagesBehind.map((page, index) => (
                <React.Fragment key={index}>
                    {index > 0 && <ArrowRight className="bread-crumbs-arrow" height={24} width={24} />}
                    <a href={page.pageUrl} className="bread-crumbs-page-link">{page.pageName}</a>
                </React.Fragment>
            ))}

            {pagesBehind.length > 0 && (
                <ArrowRight className="bread-crumbs-arrow" height={24} width={24} />
            )}

            <span className="bread-crumbs-current-page-name">{currentPageName}</span>
        </div>
    );
}