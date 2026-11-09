// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://blog.dh6k.vip',
	integrations: [mdx(), sitemap()],
	fonts: [
		{
			provider: fontProviders.local(),
			name: 'Major Mono Display',
			cssVariable: '--font-mono-display',
			fallbacks: ['ui-monospace', 'monospace'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/major-mono-display-400-normal.woff2'],
						weight: 400,
						style: 'normal',
						display: 'swap',
					},
				],
			},
		},
		{
			provider: fontProviders.local(),
			name: 'Beth Ellen',
			cssVariable: '--font-hand',
			fallbacks: ['cursive'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/beth-ellen-400-normal.woff2'],
						weight: 400,
						style: 'normal',
						display: 'swap',
					},
				],
			},
		},
		{
			provider: fontProviders.local(),
			name: 'Lexend',
			cssVariable: '--font-display',
			fallbacks: ['system-ui', 'sans-serif'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/lexend-400-normal.woff2'],
						weight: '400 600',
						style: 'normal',
						display: 'swap',
					},
				],
			},
		},
		{
			provider: fontProviders.local(),
			name: 'Maven Pro',
			cssVariable: '--font-head',
			fallbacks: ['system-ui', 'sans-serif'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/maven-pro-500-normal.woff2'],
						weight: '500 700',
						style: 'normal',
						display: 'swap',
					},
				],
			},
		},
		{
			provider: fontProviders.local(),
			name: 'Asap',
			cssVariable: '--font-body',
			fallbacks: ['system-ui', 'sans-serif'],
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/asap-400-normal.woff2'],
						weight: 400,
						style: 'normal',
						display: 'swap',
					},
					{
						src: ['./src/assets/fonts/asap-400-italic.woff2'],
						weight: 400,
						style: 'italic',
						display: 'swap',
					},
				],
			},
		},
	],
});
